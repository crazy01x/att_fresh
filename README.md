# fresh-updates

Base repository structure for receiving and validating Fresh platform updates (app + language runtime).

## What this repository provides
- Standard folders for app and language manifests.
- Sync script to download manifests from configured sources.
- Manifest validator and unit tests.
- CI pipeline for pull requests and pushes to `main`.
- Scheduled automation to open PRs with synced manifests.
- PR template and CODEOWNERS for stricter reviews.

## Repository structure
- `/updates/app/manifest.json`: app update manifest.
- `/updates/language/manifest.json`: language/runtime update manifest.
- `/scripts/sync_updates.py`: fetches remote manifests and updates local files.
- `/scripts/validate_manifests.py`: enforces manifest format and consistency.
- `/.github/workflows/ci.yml`: validation + tests.
- `/.github/workflows/auto-sync.yml`: scheduled sync and PR creation.

## Quick start
1. Copy the source template:
   - `cp config/sources.example.json config/sources.json`
2. Set real endpoint URLs in `config/sources.json`.
3. Run sync:
   - `python scripts/sync_updates.py --sources config/sources.json`
4. Validate:
   - `python scripts/validate_manifests.py`
   - `python -m unittest discover -s tests -p "test_*.py"`

## Automation secret
Set the repository secret below so the scheduled workflow can sync updates:
- `FRESH_UPDATE_SOURCES_JSON`: full JSON content matching `config/sources.example.json`.
