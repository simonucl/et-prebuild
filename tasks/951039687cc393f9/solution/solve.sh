#!/bin/bash
set -euo pipefail

repo=/home/user/archive_lab/repo
out=/home/user/archive_lab/out
archive=ledger-agent-2.1.0.tar.gz
tag=v2.1.0
prefix=ledger-agent-2.1.0/

rm -rf "$out"
mkdir -p "$out"

git -C "$repo" archive --format=tar --prefix="$prefix" "$tag" | gzip -9 -n > "$out/$archive"

sha=$(sha256sum "$out/$archive" | awk '{print $1}')
printf '%s  %s\n' "$sha" "$archive" > "$out/$archive.sha256"

commit=$(git -C "$repo" rev-parse "$tag^{commit}")
entries_json=$(git -C "$repo" archive --format=tar --prefix="$prefix" "$tag" | tar -tf - | python3 -c 'import json,sys; print(json.dumps([line.rstrip("\n") for line in sys.stdin], separators=(",", ":")))') 

python3 - "$out/manifest.json" "$archive" "$tag" "$prefix" "$commit" "$sha" "$entries_json" <<'PY'
import json
import sys

path, archive, tag, prefix, commit, sha, entries_json = sys.argv[1:]
manifest = {
    "archive": archive,
    "tag": tag,
    "prefix": prefix,
    "git_commit": commit,
    "gzip": "gzip -9 -n",
    "sha256": sha,
    "entries": json.loads(entries_json),
}
with open(path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(manifest, f, separators=(",", ":"))
    f.write("\n")
PY
