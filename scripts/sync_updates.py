#!/usr/bin/env python3
"""Download update manifests for app and language components."""

from __future__ import annotations

import argparse
import json
import pathlib
import urllib.request


REQUIRED_KEYS = {"app", "language"}


def load_sources(path: pathlib.Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise ValueError(f"Missing source configuration for: {', '.join(sorted(missing))}")
    return data


def download_manifest(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:  # nosec B310
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def store_manifest(manifest: dict, destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync update manifests.")
    parser.add_argument(
        "--sources",
        default="config/sources.json",
        help="Path to source config JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sources_path = pathlib.Path(args.sources)
    if not sources_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {sources_path}. Copy config/sources.example.json first."
        )

    sources = load_sources(sources_path)
    targets = {
        "app": pathlib.Path("updates/app/manifest.json"),
        "language": pathlib.Path("updates/language/manifest.json"),
    }

    for key, target in targets.items():
        manifest = download_manifest(sources[key]["url"])
        store_manifest(manifest, target)
        print(f"Updated {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
