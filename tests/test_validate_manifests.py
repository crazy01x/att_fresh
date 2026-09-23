import json
import pathlib
import tempfile
import unittest

from scripts.validate_manifests import validate_manifest


class ValidateManifestTest(unittest.TestCase):
    def test_valid_manifest(self) -> None:
        payload = {
            "channel": "stable",
            "latest_version": "1.0.0",
            "releases": [
                {
                    "version": "1.0.0",
                    "published_at": "2026-01-01T00:00:00Z",
                    "notes": "Initial release",
                    "artifact_url": "https://example.com/artifact.zip",
                    "checksum_sha256": "abc123",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = pathlib.Path(tmpdir) / "manifest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(validate_manifest(path), [])

    def test_invalid_manifest_missing_release_keys(self) -> None:
        payload = {
            "channel": "stable",
            "latest_version": "1.0.0",
            "releases": [{"version": "1.0.0"}],
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = pathlib.Path(tmpdir) / "manifest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            errors = validate_manifest(path)
            self.assertTrue(any("missing keys" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
