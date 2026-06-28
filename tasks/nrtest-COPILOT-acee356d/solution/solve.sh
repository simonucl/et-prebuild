#!/bin/bash
set -e

mkdir -p /home/user/reports
chmod 755 /home/user/reports

python3 - <<'PYEOF'
import os, json, glob, datetime

REG = "/home/user/registry"

def parse(v):
    if '-' in v:
        core, pre = v.split('-', 1); pre_ids = pre.split('.')
    else:
        core, pre_ids = v, None
    a, b, c = (int(x) for x in core.split('.'))
    return a, b, c, pre_ids

def prec(v):
    a, b, c, pre = parse(v)
    if pre is None:
        pk = (1,)
    else:
        ids = []
        for ident in pre:
            if ident.isdigit():
                ids.append((0, int(ident), ''))
            else:
                ids.append((1, 0, ident))
        pk = (0, tuple(ids))
    return (a, b, c, pk)

# Read registry
pkgs = {}
for path in glob.glob(os.path.join(REG, "*.meta")):
    base = os.path.basename(path)[:-len(".meta")]
    name, ver = base.split("@", 1)
    meta = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            k, val = line.split("=", 1)
            meta[k] = val
    size = int(meta["size_bytes"])
    yanked = meta["yanked"].lower() == "true"
    pkgs.setdefault(name, []).append((ver, size, yanked))

packages = []
total = 0
for name in sorted(pkgs):
    vers = pkgs[name]
    stable = [(v, s, y) for (v, s, y) in vers if (not y) and parse(v)[3] is None]
    latest = max(stable, key=lambda t: prec(t[0]))[0]
    superseded = []
    for v, s, y in sorted(vers, key=lambda t: prec(t[0])):
        if v == latest:
            continue
        if y:
            reason = "yanked"
        elif parse(v)[3] is not None:
            reason = "prerelease"
        else:
            reason = "older"
        superseded.append({"version": v, "reason": reason, "size_bytes": s})
    reclaim_entries = [e for e in superseded if e["reason"] in ("older", "yanked")]
    reclaimable = sum(e["size_bytes"] for e in reclaim_entries)
    total += reclaimable
    packages.append({
        "name": name,
        "candidates_considered": len(vers),
        "latest_stable": latest,
        "superseded": superseded,
        "reclaimable_bytes": reclaimable,
        "_k": len(reclaim_entries),
    })

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

doc = {
    "registry": REG,
    "generated_at": now,
    "packages": [{k: p[k] for k in ("name", "candidates_considered", "latest_stable", "superseded", "reclaimable_bytes")} for p in packages],
    "total_reclaimable_bytes": total,
}

with open("/home/user/reports/upgrade_plan.json", "w") as f:
    f.write(json.dumps(doc, separators=(",", ":")) + "\n")

lines = []
for p in packages:
    lines.append(f"{p['name']} keep {p['latest_stable']} reclaim {p['reclaimable_bytes']} bytes from {p['_k']} artefact(s)")
lines.append(f"TOTAL reclaimable {total} bytes")
with open("/home/user/reports/upgrade_plan.log", "w") as f:
    f.write("\n".join(lines) + "\n")
PYEOF

echo "Oracle wrote upgrade_plan.json and upgrade_plan.log"
