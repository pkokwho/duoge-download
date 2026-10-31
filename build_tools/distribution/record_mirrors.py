"""Persist real publication evidence and the required per-push project memory."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

START = "<!-- automatic-mirrors:start -->"
END = "<!-- automatic-mirrors:end -->"


def mirror_links(result):
    files = {}
    for entry in result["releases"].values():
        mirror = entry.get("sourceforge", {})
        if mirror.get("status") != "verified":
            continue
        url = urlsplit(mirror.get("url", ""))
        expected = r"/projects/[a-z0-9][a-z0-9-]{1,59}/files/" + re.escape(entry["tag"]) + "/" + re.escape(entry["filename"]) + "/download"
        if entry.get("github", {}).get("status") != "verified" or mirror.get("sha256") != entry["sha256"] or mirror.get("size_bytes") != entry["size_bytes"] or url.scheme != "https" or url.hostname != "sourceforge.net" or url.username or url.password or url.query or url.fragment or url.port not in (None, 443) or not re.fullmatch(expected, url.path):
            raise ValueError("Refusing to advertise an unverified or mismatched mirror")
        files[entry["filename"]] = {"url": mirror["url"], "sha256": entry["sha256"], "size_bytes": entry["size_bytes"], "version_name": entry["version_name"], "verified_at": mirror["verified_at"]}
    return {"schema_version": 1, "files": files}


def record(root, result_path):
    root = Path(root)
    result = json.loads(Path(result_path).read_text())
    if result.get("schema_version") != 1 or result.get("production_channels_changed") is not False:
        raise ValueError("Invalid distribution evidence")
    if not result.get("releases") or any(r.get("github", {}).get("status") != "verified" for r in result["releases"].values()):
        raise ValueError("Cannot record unverified GitHub releases as published")
    links = mirror_links(result)
    lines = [START, "## Automatic release mirror evidence", "- This section is maintained after actual publication/download checks; original website/update channels are not promoted."]
    for entry in sorted(result["releases"].values(), key=lambda r: r["version_code"])[-3:]:
        lines.append(f"- {entry['version_name']} / {entry['version_code']}: GitHub asset verified ({entry['sha256']}); SourceForge {entry['sourceforge']['status']}.")
    lines += ["- SourceForge requires account-owner GitHub Integration authorization once; no manual APK uploads or SSH secrets for ongoing synchronization. Mainland speed remains untested until phone measurement.", "- Full immutable artifact identities and verified URLs: distribution/mirror-status.json. GitHub Actions publication run is available in repository Actions; current handoff commit via git log -1.", END]
    state_path = root / "docs/agent/STATE.md"
    state = state_path.read_text()
    section = "\n".join(lines)
    if START in state:
        if END not in state:
            raise ValueError("Incomplete mirror memory marker")
        state = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: section, state, count=1, flags=re.S)
    else:
        state = state.rstrip() + "\n\n" + section + "\n"
    if len(state.splitlines()) > 80:
        raise ValueError("Project memory exceeds 80 lines; compact it before release")
    (root / "distribution/mirror-status.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    if (root / "index.html").exists():
        (root / "mirror-links.json").write_text(json.dumps(links, ensure_ascii=False, indent=2) + "\n")
    state_path.write_text(state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--result", required=True, type=Path)
    args = parser.parse_args()
    record(args.root, args.result)
