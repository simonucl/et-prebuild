#!/bin/bash
set -u

mkdir -p /logs/verifier
reward_file=/logs/verifier/reward.txt

fail() {
  echo "FAIL: $1"
  echo 0 > "$reward_file"
  exit 0
}

repo=/home/user/archive_lab/repo
out=/home/user/archive_lab/out
archive=ledger-agent-2.1.0.tar.gz
tag=v2.1.0
prefix=ledger-agent-2.1.0/

[ -d "$repo/.git" ] || fail "repository is missing or no longer a Git repository"
[ -d "$out" ] || fail "output directory is missing"

actual_files=$(find "$out" -mindepth 1 -maxdepth 1 -printf '%f\n' | LC_ALL=C sort | tr '\n' ' ')
expected_files="ledger-agent-2.1.0.tar.gz ledger-agent-2.1.0.tar.gz.sha256 manifest.json "
[ "$actual_files" = "$expected_files" ] || fail "output directory contains unexpected files: $actual_files"

[ -f "$out/$archive" ] || fail "archive is missing"
[ -f "$out/$archive.sha256" ] || fail "checksum file is missing"
[ -f "$out/manifest.json" ] || fail "manifest is missing"

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

if ! git -C "$repo" diff --quiet || [ -n "$(git -C "$repo" status --porcelain=v1)" ]; then
  fail "repository has been modified"
fi

if ! git -C "$repo" rev-parse --verify "$tag^{commit}" >/dev/null 2>&1; then
  fail "tag v2.1.0 is missing or invalid"
fi

git -C "$repo" archive --format=tar --prefix="$prefix" "$tag" > "$tmpdir/expected.tar" || fail "could not create expected tar stream"
gzip -9 -n < "$tmpdir/expected.tar" > "$tmpdir/expected.tar.gz" || fail "could not create expected gzip stream"

cmp -s "$out/$archive" "$tmpdir/expected.tar.gz" || fail "archive does not match git archive piped through gzip -9 -n"

sha=$(sha256sum "$out/$archive" | awk '{print $1}')
printf '%s  %s\n' "$sha" "$archive" > "$tmpdir/expected.sha256"
cmp -s "$out/$archive.sha256" "$tmpdir/expected.sha256" || fail "checksum file content is incorrect"

if gzip -dc "$out/$archive" | tar -tf - | grep -E '(^|/)(dist|scratch)(/|$)|\.tmp$' >/dev/null; then
  fail "archive contains files that .gitattributes should export-ignore"
fi

if ! gzip -dc "$out/$archive" | tar -xOf - "${prefix}README.md" | grep -Eq '^Revision: [0-9a-f]{40}$'; then
  fail "README.md did not receive git archive export-subst expansion"
fi

commit=$(git -C "$repo" rev-parse "$tag^{commit}")
entries_json=$(tar -tf "$tmpdir/expected.tar" | python3 -c 'import json,sys; print(json.dumps([line.rstrip("\n") for line in sys.stdin], separators=(",", ":")))') || fail "could not compute expected entries"

python3 - "$tmpdir/expected_manifest.json" "$archive" "$tag" "$prefix" "$commit" "$sha" "$entries_json" <<'PY' || fail "could not write expected manifest"
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

cmp -s "$out/manifest.json" "$tmpdir/expected_manifest.json" || fail "manifest content, key order, minification, or trailing newline is incorrect"

echo 1 > "$reward_file"
exit 0
