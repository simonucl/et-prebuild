#!/bin/bash
set -euo pipefail

repo=/home/circleci/widget-service
release_dir=/home/circleci/releases
archive_name=widget-service-1.4.2.tar.gz
manifest_name=widget-service-1.4.2.manifest.json

cd "$repo"

cat > .gitattributes <<'EOF'
tests/ export-ignore
docs/draft.md export-ignore
.env.sample export-ignore
.ci/ export-ignore
build/ export-ignore
EOF

git add .gitattributes
git commit -q -m "Add release archive exclusions"

mkdir -p "$release_dir"
git archive \
  --format=tar.gz \
  --prefix=widget-service-1.4.2/ \
  -o "$release_dir/$archive_name" \
  HEAD

python3 - <<'PY'
import hashlib
import json
import os
import subprocess
import tarfile
from pathlib import Path

repo = Path("/home/circleci/widget-service")
release_dir = Path("/home/circleci/releases")
archive_name = "widget-service-1.4.2.tar.gz"
archive = release_dir / archive_name
manifest = release_dir / "widget-service-1.4.2.manifest.json"

entries = []
with tarfile.open(archive, "r:gz") as tf:
    for member in tf.getmembers():
        if member.isfile():
            entries.append(member.name)
entries.sort()

payload = {
    "package": "widget-service",
    "version": "1.4.2",
    "git_commit": subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip(),
    "archive": archive_name,
    "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
    "size_bytes": os.path.getsize(archive),
    "entries": entries,
}
manifest.write_text(json.dumps(payload, separators=(",", ":")) + "\n")
PY
