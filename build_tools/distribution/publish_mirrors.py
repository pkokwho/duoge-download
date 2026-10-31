"""Publish existing signed APKs, then verify SourceForge's official GitHub mirror.

No SourceForge password, cookie or SSH key is required. Initial account-owner
GitHub Integration authorization is required on SourceForge itself.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_catalog(path):
    data = json.loads(Path(path).read_text())
    if data.get("schema_version") != 1 or data.get("github_repository") != "pkokwho/duoge-download":
        raise ValueError("Unexpected release catalog/repository")
    pin_file = ROOT / "distribution/standalone-signer.sha256"
    if not pin_file.exists():
        pin_file = ROOT / "build_tools/android/standalone-signer.sha256"
    pin = pin_file.read_text().strip()
    if data.get("certificate_sha256") != pin or data.get("package_name") != "org.duoge.parkour.standalone":
        raise ValueError("Catalog must retain the existing standalone package and signer")
    tags, names, codes = set(), set(), set()
    for release in data["releases"]:
        if not re.fullmatch(r"v[0-9.]+-standalone", release["tag"]):
            raise ValueError("Invalid release tag")
        if not re.fullmatch(r"duoge-parkour-[0-9.]+-dev-arm64-standalone\.apk", release["filename"]):
            raise ValueError("Invalid APK filename")
        if not re.fullmatch(r"[0-9a-f]{64}", release["sha256"]) or not re.fullmatch(r"[0-9a-f]{40}", release["source_commit"]):
            raise ValueError("Invalid APK digest/source commit")
        if type(release["version_code"]) is not int or type(release["size_bytes"]) is not int or release["size_bytes"] <= 0:
            raise ValueError("Invalid release size/version")
        if type(release["prerelease"]) is not bool:
            raise ValueError("Release stability must be explicit")
        archive = release.get("source_archive", {})
        expected_code_name = "duoge-code-" + release["version_name"] + ".zip"
        if archive.get("filename") != expected_code_name or archive.get("path") != "source/" + expected_code_name or type(archive.get("size_bytes")) is not int or archive["size_bytes"] <= 0 or not re.fullmatch(r"[0-9a-f]{64}", str(archive.get("sha256", ""))):
            raise ValueError("A pinned public first-party code archive is required")
        if not re.fullmatch(r"https://raw\.githubusercontent\.com/pkokwho/duoge-download/[0-9a-f]{40}/downloads/" + re.escape(release["filename"]), release["origin_url"]):
            raise ValueError("APK origin must be an immutable public download-repo commit")
        if release.get("target_commit") != release["origin_url"].split("/")[5]:
            raise ValueError("Release tag must target the public artifact commit")
        if release["tag"] in tags or release["filename"] in names or release["version_code"] in codes:
            raise ValueError("Duplicate release identity")
        tags.add(release["tag"]); names.add(release["filename"]); codes.add(release["version_code"])
    if not tags:
        raise ValueError("Empty release catalog")
    return data


class PublicRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_download_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate_download_url(url):
    parsed = urllib.parse.urlsplit(url)
    allowed = parsed.hostname in {"github.com", "raw.githubusercontent.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com", "sourceforge.net", "downloads.sourceforge.net"}
    allowed = allowed or bool(parsed.hostname and parsed.hostname.endswith(".dl.sourceforge.net"))
    if parsed.scheme != "https" or not allowed or parsed.username or parsed.password or parsed.port not in (None, 443):
        raise ValueError("Unexpected public download destination")


def download(url, path, limit):
    validate_download_url(url)
    opener = urllib.request.build_opener(PublicRedirects())
    request = urllib.request.Request(url, headers={"User-Agent": "duoge-verified-distribution/1"})
    size = 0
    with opener.open(request, timeout=120) as response, Path(path).open("wb") as output:
        if response.status != 200:
            raise ValueError("Public download did not return HTTP 200")
        while chunk := response.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                raise ValueError("Public download exceeds expected size")
            output.write(chunk)


def verify_bytes(path, release):
    if Path(path).stat().st_size != release["size_bytes"] or sha256(path) != release["sha256"]:
        raise ValueError("APK size/SHA differs from approved signed release")


def find_android_tools(explicit=None):
    candidates = [Path(explicit)] if explicit else []
    for name in ("ANDROID_HOME", "ANDROID_SDK_ROOT"):
        if os.environ.get(name):
            candidates += sorted((Path(os.environ[name]) / "build-tools").glob("*"), reverse=True)
    for candidate in candidates:
        if (candidate / "apksigner").is_file() and (candidate / "aapt").is_file():
            return candidate
    raise ValueError("Android build-tools (apksigner and aapt) are required")


def verify_apk(path, release, catalog, tools):
    verify_bytes(path, release)
    with zipfile.ZipFile(path) as archive:
        if len(archive.namelist()) != len(set(archive.namelist())) or archive.testzip():
            raise ValueError("Invalid APK archive")
    signature = subprocess.run([str(tools / "apksigner"), "verify", "--print-certs", str(path)], capture_output=True, text=True, check=True).stdout
    if "certificate SHA-256 digest: " + catalog["certificate_sha256"] not in signature:
        raise ValueError("APK signer changed")
    info = subprocess.run([str(tools / "aapt"), "dump", "badging", str(path)], capture_output=True, text=True, check=True).stdout
    expected = f"name='{catalog['package_name']}' versionCode='{release['version_code']}' versionName='{release['version_name']}'"
    if expected not in info or "sdkVersion:'29'" not in info or "targetSdkVersion:'36'" not in info or "native-code: 'arm64-v8a'" not in info:
        raise ValueError("APK package/version/Android requirements do not match catalog")


class GitHub:
    def __init__(self, repository, token):
        self.repository, self.token = repository, token

    def call(self, method, path, body=None, binary=False):
        origin = "https://uploads.github.com/" if binary else "https://api.github.com/"
        headers = {"Authorization": "Bearer " + self.token, "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "duoge-verified-distribution/1"}
        if body is not None:
            headers["Content-Type"] = "application/octet-stream" if binary else "application/json"
        payload = body if binary or body is None else json.dumps(body).encode()
        request = urllib.request.Request(origin + path, data=payload, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 404 and method == "GET" and "/releases/tags/" in path:
                return None
            raise RuntimeError(f"GitHub API {method} failed with HTTP {error.code}") from None


def release_body(release, catalog):
    return (release["notes"] + "\n\n此镜像与官网已有安装包逐字节相同，未重新构建或签名。\n"
            "独立新版可更新0.1.5/0.1.6；不能覆盖原包名0.1.4，不自动迁移旧版纪录。\n\n"
            f"包名：{catalog['package_name']}\n版本：{release['version_name']} / {release['version_code']}\n"
            f"大小：{release['size_bytes']} bytes\nSHA-256：{release['sha256']}\n"
            f"证书SHA-256：{catalog['certificate_sha256']}\n\n"
            "第一方程序源码见随附duoge-code版本ZIP，采用MIT；肖像、美术和第三方内容保持原有许可，详见NOTICE.txt。\n"
            "镜像存在不等于已完成中国大陆速度测试。官网正式/测试状态以官网说明为准。")


def publish_release(api, release, catalog, apk, latest_tag, extra_files=None):
    base = f"repos/{api.repository}/releases"
    existing = api.call("GET", base + "/tags/" + release["tag"])
    body = release_body(release, catalog)
    name = "舵哥快跑 " + release["version_name"] + (" · 双角色测试" if release["prerelease"] else " · 正式版镜像")
    if existing is None:
        existing = api.call("POST", base, {"tag_name": release["tag"], "target_commitish": release.get("target_commit", release["source_commit"]), "name": name, "body": body, "draft": True, "prerelease": release["prerelease"]})
    release_id = int(existing["id"])
    files = {release["filename"]: Path(apk).read_bytes(), release["filename"] + ".sha256": (release["sha256"] + "  " + release["filename"] + "\n").encode(), "CODE-LICENSE.txt": (ROOT / "LICENSE").read_bytes(), "NOTICE.txt": (ROOT / "NOTICE.md").read_bytes()}
    files.update(extra_files or {})
    assets = api.call("GET", f"{base}/{release_id}/assets?per_page=100")
    by_name = {item["name"]: item for item in assets}
    for name, data in files.items():
        prior = by_name.get(name)
        if prior and not existing["draft"] and name in ("CODE-LICENSE.txt", "NOTICE.txt"):
            # Keep the legal notices frozen with their original release. Later
            # documentation/copyright changes must not rewrite old assets.
            continue
        expected = "sha256:" + hashlib.sha256(data).hexdigest()
        if prior:
            if prior["size"] != len(data) or prior.get("digest") not in (None, expected):
                raise ValueError("Existing release asset differs; refusing overwrite: " + name)
        else:
            if not existing["draft"]:
                raise ValueError("Published release lacks an asset; create a new release instead of silently appending")
            uploaded = api.call("POST", f"{base}/{release_id}/assets?" + urllib.parse.urlencode({"name": name}), data, binary=True)
            if uploaded.get("state") != "uploaded" or uploaded["size"] != len(data) or uploaded.get("digest") not in (None, expected):
                raise ValueError("Release upload verification failed")
    # Publish only AFTER every asset is attached: SourceForge's release webhook
    # does not reliably discover attachments added after publication.
    title = "舵哥快跑 " + release["version_name"] + (" · 双角色测试" if release["prerelease"] else " · 正式版镜像")
    if existing["draft"] or existing.get("body") != body or existing.get("prerelease") != release["prerelease"] or existing.get("name") != title:
        api.call("PATCH", f"{base}/{release_id}", {"draft": False, "name": title, "prerelease": release["prerelease"], "body": body, "make_latest": "true" if release["tag"] == latest_tag else "false"})
    return f"https://github.com/{api.repository}/releases/download/{release['tag']}/{release['filename']}"


def verify_sourceforge(config, release, directory, prior=None, attempts=1):
    if not config.get("enabled"):
        return {"status": "awaiting_account_owner_authorization"}
    project = config.get("project")
    if not isinstance(project, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,59}", project):
        raise ValueError("Invalid SourceForge project name")
    url = f"https://sourceforge.net/projects/{project}/files/{release['tag']}/{release['filename']}/download"
    if prior and prior.get("status") == "verified" and prior.get("url") == url and prior.get("sha256") == release["sha256"]:
        return prior
    for attempt in range(attempts):
        try:
            target = directory / ("sourceforge-" + release["filename"])
            download(url, target, release["size_bytes"])
            verify_bytes(target, release)
            return {"status": "verified", "url": url, "sha256": release["sha256"], "size_bytes": release["size_bytes"], "verified_at": stamp()}
        except (OSError, ValueError):
            if attempt + 1 < attempts:
                time.sleep(20)
    # Never advertise an expected-but-unverified URL as a working mirror.
    return {"status": "pending_import_or_verification", "project": project}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=ROOT / "distribution/releases.json")
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--build-tools")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--mirror-only", action="store_true")
    parser.add_argument("--mirror-attempts", type=int, default=1, choices=range(1, 7))
    args = parser.parse_args()
    catalog = load_catalog(args.catalog)
    config = json.loads((ROOT / "distribution/sourceforge.json").read_text())
    old_path = ROOT / "distribution/mirror-status.json"
    old = json.loads(old_path.read_text()) if old_path.exists() else {"releases": {}}
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    records = {}
    tools = None if args.mirror_only else find_android_tools(args.build_tools)
    stable = [item for item in catalog["releases"] if not item["prerelease"]]
    latest = max(stable, key=lambda item: item["version_code"])["tag"] if stable else None
    token = os.environ.get("GH_TOKEN")
    if not args.preflight and not args.mirror_only and not token:
        parser.error("GH_TOKEN must be provided securely through the workflow environment")
    api = GitHub(catalog["github_repository"], token) if token else None
    if api and not args.preflight and not args.mirror_only:
        if api.call("GET", "repos/" + api.repository).get("private") is not False:
            raise ValueError("Release destination must be publicly accessible; refusing private-repo publication")
    for release in catalog["releases"]:
        prior = old.get("releases", {}).get(release["tag"], {})
        record = {key: release[key] for key in ("tag", "version_name", "version_code", "filename", "size_bytes", "sha256", "prerelease")}
        if not args.mirror_only:
            path = args.artifact_dir / release["filename"]
            if not path.exists():
                download(release["origin_url"], path, release["size_bytes"])
            verify_apk(path, release, catalog, tools)
            archive = release["source_archive"]
            code = ROOT / archive["path"]
            if not code.is_file():
                code = args.artifact_dir / archive["filename"]
            if code.stat().st_size != archive["size_bytes"] or sha256(code) != archive["sha256"]:
                raise ValueError("Public code archive differs from approved snapshot")
            if args.preflight:
                record["github"] = {"status": "local_apk_verified_not_published"}
            else:
                extra = {archive["filename"]: code.read_bytes()}
                url = publish_release(api, release, catalog, path, latest, extra)
                public = args.artifact_dir / ("github-" + release["filename"])
                download(url, public, release["size_bytes"])
                verify_bytes(public, release)
                record["github"] = prior.get("github") if prior.get("sha256") == release["sha256"] and prior.get("github", {}).get("status") == "verified" else {"status": "verified", "url": url, "verified_at": stamp()}
        else:
            if prior.get("sha256") != release["sha256"] or prior.get("github", {}).get("status") != "verified":
                raise ValueError("Publish and verify GitHub asset before mirror-only checks")
            record["github"] = prior["github"]
        record["sourceforge"] = {"status": "not_checked_in_preflight"} if args.preflight else verify_sourceforge(config, release, args.artifact_dir, prior.get("sourceforge"), args.mirror_attempts)
        records[release["tag"]] = record
        print(release["tag"], record["github"]["status"], record["sourceforge"]["status"], flush=True)
    result = {"schema_version": 1, "github_repository": catalog["github_repository"], "certificate_sha256": catalog["certificate_sha256"], "production_channels_changed": False, "releases": records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
