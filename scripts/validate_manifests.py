#!/usr/bin/env python3
"""Validate update manifests used by the update pipeline."""

from __future__ import annotations

import json
import pathlib


MANIFESTS = [
    pathlib.Path("updates/app/manifest.json"),
    pathlib.Path("updates/language/manifest.json"),
]
REQUIRED_TOP_LEVEL = {"channel", "latest_version", "releases"}
REQUIRED_RELEASE = {"version", "published_at", "notes", "artifact_url", "checksum_sha256"}


def validate_manifest(path: pathlib.Path) -> list[str]:
    errors: list[str] = []

    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"Missing manifest: {path}"]
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in {path}: {exc}"]

    missing = REQUIRED_TOP_LEVEL - content.keys()
    if missing:
        errors.append(f"{path}: missing top-level keys: {', '.join(sorted(missing))}")

    releases = content.get("releases")
    if not isinstance(releases, list):
        errors.append(f"{path}: releases must be a list")
        return errors

    latest = content.get("latest_version")
    if releases and latest != releases[0].get("version"):
        errors.append(
            f"{path}: latest_version must match first release version ({releases[0].get('version')})"
        )

    for idx, release in enumerate(releases):
        if not isinstance(release, dict):
            errors.append(f"{path}: releases[{idx}] must be an object")
            continue
        release_missing = REQUIRED_RELEASE - release.keys()
        if release_missing:
            errors.append(
                f"{path}: releases[{idx}] missing keys: {', '.join(sorted(release_missing))}"
            )

    return errors


def main() -> int:
    errors: list[str] = []
    for manifest in MANIFESTS:
        errors.extend(validate_manifest(manifest))

    if errors:
        for error in errors:
            print(error)
        return 1

    print("All manifests are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
