#!/bin/bash
set -euo pipefail

lab=/home/user/rsync-lab
handoff="$lab/handoff"

rm -rf "$handoff"
mkdir -p "$handoff"

rsync -a --delete "$lab/baseline/site/" "$lab/receiver/site/"
rsync -a --delete --checksum --itemize-changes \
  --write-batch="$handoff/site-update.batch" \
  "$lab/desired/site/" "$lab/receiver/site/" \
  > "$handoff/itemized-changes.txt"

rm -f "$handoff/site-update.batch.sh"
cat > "$handoff/apply-site-update.sh" <<'SH'
#!/bin/bash
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "usage: apply-site-update.sh DEST_DIR" >&2
  exit 2
fi
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
dest=$1
rsync -a --delete --checksum --itemize-changes --read-batch="$script_dir/site-update.batch" "$dest"
SH
chmod 0755 "$handoff/apply-site-update.sh"
chmod 0600 "$handoff/site-update.batch"
chmod 0644 "$handoff/itemized-changes.txt"

python3 - <<'PY'
import hashlib
import json
from pathlib import Path

handoff = Path("/home/user/rsync-lab/handoff")
batch = handoff / "site-update.batch"
changes = (handoff / "itemized-changes.txt").read_text().splitlines()
manifest = {
    "batch": "site-update.batch",
    "apply_script": "apply-site-update.sh",
    "source_root": "site/",
    "options": ["-a", "--delete", "--checksum", "--itemize-changes"],
    "changes": changes,
    "batch_sha256": hashlib.sha256(batch.read_bytes()).hexdigest(),
}
(handoff / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
PY
chmod 0644 "$handoff/manifest.json"
