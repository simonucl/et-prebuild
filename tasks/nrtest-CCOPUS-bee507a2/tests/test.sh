#!/bin/bash
# Deterministic verifier. Independently recomputes the canonical manifest +
# reclaim report from the untouched read-only input using Debian version
# ordering (dpkg), then byte-compares the agent's output. Writes the reward to
# EXACTLY /logs/verifier/reward.txt.
set -u
mkdir -p /logs/verifier

python3 - <<'PY'
import csv, json, functools, subprocess, os, sys

SRC = "/home/user/pool/builds.tsv"
OUT = "/home/user/out"
errors = []

def fail(m):
    errors.append(m)

def dcmp(a, b):
    if a == b:
        return 0
    if subprocess.run(["dpkg", "--compare-versions", a, "lt", b]).returncode == 0:
        return -1
    return 1

# --- recompute canonical expected output from the read-only input ---
groups = {}
nbuilds = 0
try:
    with open(SRC, newline="") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            groups.setdefault((row["package"], row["arch"]), []).append(
                (row["version"], int(row["size_bytes"]))
            )
            nbuilds += 1
except Exception as e:
    fail(f"could not read input: {e}")

group_objs, report_lines = [], []
total_reclaim = total_superseded = 0
for key in sorted(groups.keys()):
    builds = groups[key]
    builds.sort(key=functools.cmp_to_key(lambda x, y: dcmp(x[0], y[0])))
    versions = [v for v, _ in builds]
    superseded = versions[:-1]
    reclaim = sum(s for _, s in builds[:-1])
    total_reclaim += reclaim
    total_superseded += len(superseded)
    group_objs.append({
        "package": key[0], "arch": key[1], "latest": versions[-1],
        "count": len(versions), "versions": versions,
        "superseded": superseded, "reclaimable_bytes": reclaim,
    })
    report_lines.append(
        f"{key[0]}/{key[1]}: keep {versions[-1]}, supersede {len(superseded)}, reclaim {reclaim} bytes"
    )

manifest = {
    "source": SRC, "groups": group_objs,
    "totals": {"groups": len(group_objs), "builds": nbuilds, "reclaimable_bytes": total_reclaim},
}
exp_json = (json.dumps(manifest, separators=(",", ":")) + "\n").encode()
report_lines.append(f"TOTAL: {total_superseded} builds, {total_reclaim} bytes")
exp_report = ("\n".join(report_lines) + "\n").encode()

# --- input must be untouched ---
if nbuilds != 20:
    fail(f"input row count changed: {nbuilds} != 20")

# --- check manifest.json byte-for-byte ---
mp = os.path.join(OUT, "manifest.json")
if not os.path.isfile(mp):
    fail("manifest.json missing")
else:
    got = open(mp, "rb").read()
    if got != exp_json:
        fail("manifest.json content mismatch")

# --- check reclaim.txt byte-for-byte ---
rp = os.path.join(OUT, "reclaim.txt")
if not os.path.isfile(rp):
    fail("reclaim.txt missing")
else:
    got = open(rp, "rb").read()
    if got != exp_report:
        fail("reclaim.txt content mismatch")

if errors:
    sys.stderr.write("VERIFIER FAIL:\n" + "\n".join(errors) + "\n")
    sys.exit(1)
print("VERIFIER OK")
sys.exit(0)
PY

if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
