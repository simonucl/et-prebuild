#!/bin/bash
set -euo pipefail

repo=/home/user/work/telemetry-agent
out=/home/user/delivery
bundle=telemetry-agent-1.7.3.bundle
patch_archive=telemetry-agent-1.7.3-patches.tar.gz
branch=refs/heads/release/1.7.3
tag=refs/tags/v1.7.3
base=v1.7.0

rm -rf "$out"
mkdir -p "$out"

git -C "$repo" bundle create "$out/$bundle" "$branch" "$tag" "^$base"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/patches"
git -C "$repo" format-patch --no-stat --no-signature --output-directory "$tmp/patches" "$base..$branch" >/dev/null
tar --sort=name \
  --mtime='2026-02-10 00:00:00 UTC' \
  --owner=0 --group=0 --numeric-owner \
  --owner=root --group=root \
  -C "$tmp" -cf "$tmp/patches.tar" patches
gzip -n -9 < "$tmp/patches.tar" > "$out/$patch_archive"

base_commit=$(git -C "$repo" rev-parse "$base^{commit}")
release_commit=$(git -C "$repo" rev-parse "$branch^{commit}")
bundle_sha=$(sha256sum "$out/$bundle" | awk '{print $1}')
patch_sha=$(sha256sum "$out/$patch_archive" | awk '{print $1}')

python3 - "$repo" "$out/manifest.json" "$bundle" "$patch_archive" "$branch" "$tag" "$base" "$base_commit" "$release_commit" "$bundle_sha" "$patch_sha" <<'PY'
import json
import subprocess
import sys
from collections import OrderedDict

repo, manifest_path, bundle, patch_archive, branch, tag, base, base_commit, release_commit, bundle_sha, patch_sha = sys.argv[1:]
log = subprocess.check_output(
    ["git", "-C", repo, "log", "--reverse", "--format=%H%x00%s", f"{base}..{branch}"],
    text=True,
)
commits = []
for line in log.splitlines():
    commit, subject = line.split("\0", 1)
    commits.append(OrderedDict([("commit", commit), ("subject", subject)]))

manifest = OrderedDict([
    ("bundle", bundle),
    ("patch_archive", patch_archive),
    ("source_branch", branch),
    ("release_tag", tag),
    ("base_tag", base),
    ("prerequisite_commit", base_commit),
    ("release_commit", release_commit),
    ("included_commits", commits),
    ("patches", [
        "0001-Bump-release-version-to-1.7.3.patch",
        "0002-Normalize-event-kinds-for-release.patch",
        "0003-Tighten-telemetry-defaults.patch",
    ]),
    ("bundle_sha256", bundle_sha),
    ("patch_archive_sha256", patch_sha),
])
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, separators=(",", ":"))
    f.write("\n")
PY

