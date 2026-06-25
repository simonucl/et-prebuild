#!/bin/bash
set -euo pipefail

src=/home/user/release_src/gateway-agent-2.7.0
out=/home/user/handoff
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$out"
rm -f "$out/gateway-agent-2.7.0.tar.gz" "$out/manifest.json"

stage="$tmp/stage/gateway-agent-2.7.0"
mkdir -p "$stage/bin" "$stage/docs" "$stage/etc/gateway-agent" "$stage/lib/systemd/system"

cp -p "$src/LICENSE" "$stage/LICENSE"
cp -p "$src/README.md" "$stage/README.md"
cp -p "$src/bin/gateway-agent" "$stage/bin/gateway-agent"
cp -p "$src/docs/runbook.md" "$stage/docs/runbook.md"
ln -s "$(readlink "$src/docs/current")" "$stage/docs/current"
cp -p "$src/etc/gateway-agent/config.yaml" "$stage/etc/gateway-agent/config.yaml"
cp -p "$src/lib/systemd/system/gateway-agent.service" "$stage/lib/systemd/system/gateway-agent.service"

find "$stage" -type d -exec chmod 0755 {} +
find "$stage" -type f -exec chmod 0644 {} +
chmod 0755 "$stage/bin/gateway-agent"

(
  cd "$tmp/stage"
  LC_ALL=C tar --sort=name \
    --mtime='2024-02-03 04:05:06 UTC' \
    --owner=0 --group=0 --numeric-owner \
    --format=gnu \
    -cf - gateway-agent-2.7.0 | gzip -9 -n > "$out/gateway-agent-2.7.0.tar.gz"
)

python3 - <<'PY'
import hashlib
import json
from pathlib import Path

src = Path("/home/user/release_src/gateway-agent-2.7.0")
out = Path("/home/user/handoff")
archive = out / "gateway-agent-2.7.0.tar.gz"

regular = [
    ("LICENSE", "0644"),
    ("README.md", "0644"),
    ("bin/gateway-agent", "0755"),
    ("docs/runbook.md", "0644"),
    ("etc/gateway-agent/config.yaml", "0644"),
    ("lib/systemd/system/gateway-agent.service", "0644"),
]

contents = []
for rel, mode in sorted(regular):
    data = (src / rel).read_bytes()
    contents.append({
        "path": rel,
        "type": "file",
        "mode": mode,
        "sha256": hashlib.sha256(data).hexdigest(),
    })
contents.append({
    "path": "docs/current",
    "type": "symlink",
    "target": "runbook.md",
})
contents.sort(key=lambda item: item["path"])

manifest = {
    "name": "gateway-agent",
    "version": "2.7.0",
    "archive": archive.name,
    "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
    "contents": contents,
}
out.joinpath("manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
PY
