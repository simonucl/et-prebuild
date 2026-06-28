#!/bin/bash
# Deterministic verifier. Recomputes the canonical manifest + report from the
# untouched input and byte-compares the agent's output. Writes reward to
# EXACTLY /logs/verifier/reward.txt.
set -u
mkdir -p /logs/verifier

python3 - <<'PY'
import os, re, json, hashlib, stat, sys

INC = "/home/user/artifacts/incoming"
OUT = "/home/user/artifacts/out"
errors = []

def fail(msg):
    errors.append(msg)

# --- recompute canonical expected ---
pat = re.compile(r'^([a-z0-9]+)-(\d+(?:\.\d+){1,2})-(x86_64|aarch64)\.(tar\.gz|tar\.zst|whl)$')
def vkey(v):
    p = [int(x) for x in v.split('.')]
    while len(p) < 3: p.append(0)
    return tuple(p)

groups = {}
total = 0
for fn in sorted(os.listdir(INC)):
    p = os.path.join(INC, fn)
    if not os.path.isfile(p):
        continue
    m = pat.match(fn)
    if not m:
        continue
    comp, ver, arch, ext = m.groups()
    total += 1
    data = open(p, 'rb').read()
    groups.setdefault((comp, arch), []).append({
        "version": ver, "file": fn,
        "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data),
    })

components = {}
for (comp, arch), recs in groups.items():
    recs.sort(key=lambda r: vkey(r["version"]))
    components.setdefault(comp, []).append((arch, recs[-1], recs[:-1]))

comp_objs, artifacts_superseded, bytes_superseded, report_lines = [], 0, 0, []
for comp in sorted(components):
    arch_objs = []
    for arch, keep, supersede in sorted(components[comp], key=lambda t: t[0]):
        n = len(supersede); b = sum(r["size_bytes"] for r in supersede)
        artifacts_superseded += n; bytes_superseded += b
        arch_objs.append({"arch": arch, "keep": keep, "supersede": supersede})
        report_lines.append(f"{comp}/{arch}: keep {keep['version']}, supersede {n}, reclaim {b} bytes")
    comp_objs.append({"name": comp, "architectures": arch_objs})

manifest = {
    "root": INC, "components": comp_objs,
    "totals": {"components": len(components), "artifacts_total": total,
               "artifacts_superseded": artifacts_superseded, "bytes_superseded": bytes_superseded},
}
exp_json = json.dumps(manifest, separators=(',', ':')) + "\n"
report_lines.append(f"TOTAL: {artifacts_superseded} files, {bytes_superseded} bytes")
exp_report = "\n".join(report_lines) + "\n"

# --- check output dir + perms ---
if not os.path.isdir(OUT):
    fail("output dir missing")
else:
    mode = stat.S_IMODE(os.lstat(OUT).st_mode)
    if mode != 0o755:
        fail(f"out mode is {oct(mode)} not 0o755")

# --- check manifest byte-for-byte ---
mp = os.path.join(OUT, "manifest.json")
if not os.path.isfile(mp):
    fail("manifest.json missing")
else:
    got = open(mp, "rb").read()
    if got != exp_json.encode():
        fail("manifest.json content mismatch")

# --- check reclaim report byte-for-byte ---
rp = os.path.join(OUT, "reclaim.txt")
if not os.path.isfile(rp):
    fail("reclaim.txt missing")
else:
    got = open(rp, "rb").read()
    if got != exp_report.encode():
        fail("reclaim.txt content mismatch")

# --- inputs must be untouched (10 files still present) ---
remaining = [f for f in os.listdir(INC) if pat.match(f)]
if len(remaining) != total or total == 0:
    fail("incoming artifacts modified/missing")

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
