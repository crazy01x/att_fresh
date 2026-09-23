#!/usr/bin/env bash
set -euo pipefail

files=(
  "updates/app/manifest.json"
  "updates/runtime/manifest.json"
)

for file in "${files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required manifest: $file" >&2
    exit 1
  fi

  python - <<'PY' "$file"
import json
import sys
from urllib.parse import urlparse

path = sys.argv[1]
required = [
    "channel",
    "latest_version",
    "checksum_sha256",
    "download_url",
    "published_at",
]

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

missing = [k for k in required if k not in data or str(data[k]).strip() == ""]
if missing:
    raise SystemExit(f"{path}: missing required keys: {', '.join(missing)}")

if len(str(data["checksum_sha256"])) != 64 and data["checksum_sha256"] != "REPLACE_WITH_SHA256":
    raise SystemExit(f"{path}: checksum_sha256 must be a 64-char SHA-256 or placeholder")

url = urlparse(str(data["download_url"]))
if url.scheme not in {"http", "https"} or not url.netloc:
    raise SystemExit(f"{path}: download_url must be an absolute http(s) URL")

print(f"OK: {path}")
PY
done

echo "All manifests are valid."
