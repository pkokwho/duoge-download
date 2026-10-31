"""Publication safeguards; no real remote mutation or network access."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


pub = module("publish_mirrors", "build_tools/distribution/publish_mirrors.py")
rec = module("record_mirrors", "build_tools/distribution/record_mirrors.py")


class FakeGitHub:
    repository = "pkokwho/duoge-download"

    def __init__(self, existing=None, assets=None):
        self.existing = existing
        self.assets = assets or []
        self.events = []

    def call(self, method, path, body=None, binary=False):
        self.events.append((method, path, binary))
        if method == "GET" and "/tags/" in path:
            return self.existing
        if method == "GET" and "/assets?" in path:
            return self.assets
        if method == "POST" and binary:
            name = parse_qs(urlsplit(path).query)["name"][0]
            item = {"name": name, "size": len(body), "digest": "sha256:" + hashlib.sha256(body).hexdigest(), "state": "uploaded"}
            self.assets.append(item)
            return item
        if method == "POST":
            self.existing = {**body, "id": 53}
            return self.existing
        if method == "PATCH":
            if len(self.assets) != 4:
                raise AssertionError("Published before all assets were attached")
            self.existing.update(body)
            return self.existing
        raise AssertionError((method, path))


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = pub.load_catalog(ROOT / "distribution/releases.json")
        self.release = self.catalog["releases"][0]
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.apk = self.directory / self.release["filename"]
        self.apk.write_bytes(b"test APK bytes; not a real signed application")

    def test_catalog_requires_frozen_origin_and_unique_release_identity(self):
        for change in ["branch", "duplicate"]:
            invalid = copy.deepcopy(self.catalog)
            if change == "branch":
                invalid["releases"][0]["origin_url"] = invalid["releases"][0]["origin_url"].replace("26558cad363fce6e2ae7f98b3586ada1452ee057", "main")
            else:
                invalid["releases"].append(copy.deepcopy(invalid["releases"][0]))
            path = self.directory / "bad.json"
            path.write_text(json.dumps(invalid))
            with self.assertRaises(ValueError):
                pub.load_catalog(path)

    def test_no_untrusted_or_plaintext_redirects(self):
        for url in ["http://downloads.sourceforge.net/file", "https://sourceforge.net.evil.example/file", "https://github.com:444/file", "https://user:password@github.com/file"]:
            with self.assertRaises(ValueError):
                pub.validate_download_url(url)
        pub.validate_download_url("https://release-assets.githubusercontent.com/file")
        pub.validate_download_url("https://example.dl.sourceforge.net/project/file")

    def test_draft_is_published_only_after_all_uploads(self):
        api = FakeGitHub()
        url = pub.publish_release(api, self.release, self.catalog, self.apk, self.release["tag"])
        self.assertEqual(len(api.assets), 4)
        self.assertFalse(api.existing["draft"])
        self.assertEqual(api.events[-1][0], "PATCH")
        self.assertTrue(url.endswith(self.release["filename"]))

    def test_published_release_is_immutable_and_complete(self):
        api = FakeGitHub()
        pub.publish_release(api, self.release, self.catalog, self.apk, self.release["tag"])
        api.events.clear()
        pub.publish_release(api, self.release, self.catalog, self.apk, self.release["tag"])
        self.assertEqual([e[0] for e in api.events], ["GET", "GET"])
        api.assets[0]["digest"] = "sha256:" + "0" * 64
        with self.assertRaises(ValueError):
            pub.publish_release(api, self.release, self.catalog, self.apk, self.release["tag"])
        api.assets = []
        with self.assertRaises(ValueError):
            pub.publish_release(api, self.release, self.catalog, self.apk, self.release["tag"])

    def test_mirror_advertised_only_after_full_hash_verification(self):
        with patch.object(pub, "download", side_effect=lambda u, p, n: p.write_bytes(b"HTML error page")):
            result = pub.verify_sourceforge({"enabled": True, "project": "duoge-parkour"}, self.release, self.directory)
        self.assertEqual(result["status"], "pending_import_or_verification")
        self.assertNotIn("url", result)
        result = pub.verify_sourceforge({"enabled": False}, self.release, self.directory)
        self.assertEqual(result["status"], "awaiting_account_owner_authorization")

    def test_verified_mirror_and_cache_retain_exact_identity(self):
        release = {**self.release, "size_bytes": 3, "sha256": hashlib.sha256(b"APK").hexdigest()}
        config = {"enabled": True, "project": "duoge-parkour"}
        with patch.object(pub, "download", side_effect=lambda u, p, n: p.write_bytes(b"APK")):
            result = pub.verify_sourceforge(config, release, self.directory)
        self.assertEqual(result["status"], "verified")
        with patch.object(pub, "download", side_effect=AssertionError("Unnecessary redownload")):
            self.assertEqual(pub.verify_sourceforge(config, release, self.directory, result), result)

    def test_evidence_requires_actual_publication_and_preserves_human_memory(self):
        root = self.directory
        (root / "distribution").mkdir()
        (root / "docs/agent").mkdir(parents=True)
        state = root / "docs/agent/STATE.md"
        state.write_text("# Human memory\n- Preserve current game and user's decisions.\n")
        evidence = {"schema_version": 1, "production_channels_changed": False, "releases": {self.release["tag"]: {**self.release, "github": {"status": "local_apk_verified_not_published"}, "sourceforge": {"status": "pending"}}}}
        path = root / "result.json"
        path.write_text(json.dumps(evidence))
        with self.assertRaises(ValueError):
            rec.record(root, path)
        evidence["releases"][self.release["tag"]]["github"]["status"] = "verified"
        path.write_text(json.dumps(evidence))
        rec.record(root, path)
        first = state.read_text()
        rec.record(root, path)
        self.assertEqual(first, state.read_text())
        self.assertIn("Preserve current game", first)
        self.assertEqual(first.count(rec.START), 1)
        state.write_text("unchanged\n" * 80)
        with self.assertRaises(ValueError):
            rec.record(root, path)


if __name__ == "__main__":
    unittest.main()
