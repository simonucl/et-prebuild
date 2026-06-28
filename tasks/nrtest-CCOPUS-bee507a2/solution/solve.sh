#!/bin/bash
# Oracle: compute the retention manifest using Debian version ordering (dpkg).
set -eu

mkdir -p /home/user/out

python3 - <<'PY'
import csv, json, functools, subprocess

SRC = "/home/user/pool/builds.tsv"

def dcmp(a, b):
    if a == b:
        return 0
    # dpkg --compare-versions A lt B  -> exit 0 iff A < B
    if subprocess.run(["dpkg", "--compare-versions", a, "lt", b]).returncode == 0:
        return -1
    return 1

groups = {}
nbuilds = 0
with open(SRC, newline="") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        pkg = row["package"]
        arch = row["arch"]
        ver = row["version"]
        size = int(row["size_bytes"])
        groups.setdefault((pkg, arch), []).append((ver, size))
        nbuilds += 1

group_objs = []
report_lines = []
total_reclaim = 0
total_superseded = 0

for (pkg, arch) in sorted(groups.keys()):
    builds = groups[(pkg, arch)]
    builds.sort(key=functools.cmp_to_key(lambda x, y: dcmp(x[0], y[0])))
    versions = [v for v, _ in builds]
    latest = versions[-1]
    superseded = versions[:-1]
    reclaim = sum(s for _, s in builds[:-1])
    total_reclaim += reclaim
    total_superseded += len(superseded)
    group_objs.append({
        "package": pkg,
        "arch": arch,
        "latest": latest,
        "count": len(versions),
        "versions": versions,
        "superseded": superseded,
        "reclaimable_bytes": reclaim,
    })
    report_lines.append(
        f"{pkg}/{arch}: keep {latest}, supersede {len(superseded)}, reclaim {reclaim} bytes"
    )

manifest = {
    "source": SRC,
    "groups": group_objs,
    "totals": {
        "groups": len(group_objs),
        "builds": nbuilds,
        "reclaimable_bytes": total_reclaim,
    },
}

with open("/home/user/out/manifest.json", "w") as f:
    f.write(json.dumps(manifest, separators=(",", ":")) + "\n")

report_lines.append(f"TOTAL: {total_superseded} builds, {total_reclaim} bytes")
with open("/home/user/out/reclaim.txt", "w") as f:
    f.write("\n".join(report_lines) + "\n")
PY
