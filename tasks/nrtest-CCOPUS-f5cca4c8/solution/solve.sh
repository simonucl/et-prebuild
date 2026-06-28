#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import os, re, json, hashlib

INC = "/home/user/artifacts/incoming"
OUT = "/home/user/artifacts/out"
os.makedirs(OUT, exist_ok=True)
os.chmod(OUT, 0o755)

pat = re.compile(r'^([a-z0-9]+)-(\d+(?:\.\d+){1,2})-(x86_64|aarch64)\.(tar\.gz|tar\.zst|whl)$')

def vkey(v):
    parts = [int(x) for x in v.split('.')]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)

# group[(component, arch)] = list of dicts
groups = {}
total = 0
for fn in os.listdir(INC):
    p = os.path.join(INC, fn)
    if not os.path.isfile(p):
        continue
    m = pat.match(fn)
    if not m:
        continue
    comp, ver, arch, ext = m.groups()
    total += 1
    data = open(p, 'rb').read()
    rec = {
        "version": ver,
        "file": fn,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }
    groups.setdefault((comp, arch), []).append(rec)

components = {}
for (comp, arch), recs in groups.items():
    recs.sort(key=lambda r: vkey(r["version"]))   # ascending
    keep = recs[-1]
    supersede = recs[:-1]
    components.setdefault(comp, []).append((arch, keep, supersede))

comp_objs = []
artifacts_superseded = 0
bytes_superseded = 0
report_lines = []
for comp in sorted(components):
    arch_objs = []
    for arch, keep, supersede in sorted(components[comp], key=lambda t: t[0]):
        n = len(supersede)
        b = sum(r["size_bytes"] for r in supersede)
        artifacts_superseded += n
        bytes_superseded += b
        arch_objs.append({
            "arch": arch,
            "keep": keep,
            "supersede": supersede,
        })
        report_lines.append(
            f"{comp}/{arch}: keep {keep['version']}, supersede {n}, reclaim {b} bytes"
        )
    comp_objs.append({"name": comp, "architectures": arch_objs})

manifest = {
    "root": INC,
    "components": comp_objs,
    "totals": {
        "components": len(components),
        "artifacts_total": total,
        "artifacts_superseded": artifacts_superseded,
        "bytes_superseded": bytes_superseded,
    },
}

with open(os.path.join(OUT, "manifest.json"), "w") as f:
    f.write(json.dumps(manifest, separators=(',', ':')))
    f.write("\n")

report_lines.append(f"TOTAL: {artifacts_superseded} files, {bytes_superseded} bytes")
with open(os.path.join(OUT, "reclaim.txt"), "w") as f:
    f.write("\n".join(report_lines) + "\n")
PY
