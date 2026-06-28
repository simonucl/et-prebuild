#!/bin/bash
# Deterministic verifier. Recomputes the expected ledger from the read-only
# registry and compares it (order-sensitively) to the agent's /home/user/report.json.
mkdir -p /logs/verifier

python3 - <<'PYEOF'
import os, re, json, functools, sys

ARTDIR = "/home/user/registry/artifacts"
OUT = "/home/user/report.json"
REWARD = "/logs/verifier/reward.txt"

def fail(msg):
    print("VERIFIER FAIL:", msg)
    with open(REWARD, "w") as f:
        f.write("0")
    sys.exit(0)

SEMVER = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')

def parse(v):
    m = SEMVER.match(v)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4))

def pre_key(pre):
    if pre is None:
        return None
    out = []
    for i in pre.split('.'):
        if i.isdigit():
            out.append((0, int(i), ''))
        else:
            out.append((1, 0, i))
    return out

def cmp_prec(a, b):
    for x, y in zip(a[:3], b[:3]):
        if x < y: return -1
        if x > y: return 1
    pa, pb = a[3], b[3]
    if pa is None and pb is None: return 0
    if pa is None: return 1
    if pb is None: return -1
    ka, kb = pre_key(pa), pre_key(pb)
    for ia, ib in zip(ka, kb):
        if ia < ib: return -1
        if ia > ib: return 1
    if len(ka) < len(kb): return -1
    if len(ka) > len(kb): return 1
    return 0

def order_desc(versions):
    def comparator(v1, v2):
        c = cmp_prec(parse(v1), parse(v2))
        if c != 0:
            return -c
        if v1 < v2: return -1
        if v1 > v2: return 1
        return 0
    return sorted(versions, key=functools.cmp_to_key(comparator))

# --- expected -----------------------------------------------------------
valid = {}
quarantined = []
for fn in os.listdir(ARTDIR):
    if not fn.endswith('.bin'):
        continue
    stem = fn[:-4]
    if '@' not in stem:
        continue
    name, _, ver = stem.partition('@')
    if parse(ver) is None:
        quarantined.append(f"{name}@{ver}")
    else:
        valid.setdefault(name, []).append(ver)

packages = []
for name in sorted(valid.keys()):
    ordered = order_desc(valid[name])
    packages.append({
        "name": name,
        "latest": ordered[0],
        "ordered": ordered,
        "count": len(ordered),
    })
expected = {
    "registry": ARTDIR,
    "packages": packages,
    "quarantined": sorted(quarantined),
}

# --- actual -------------------------------------------------------------
if not os.path.exists(OUT):
    fail("/home/user/report.json does not exist")
try:
    with open(OUT) as f:
        actual = json.load(f)
except Exception as e:
    fail(f"report.json is not valid JSON: {e}")

if not isinstance(actual, dict):
    fail("top-level JSON is not an object")

if actual.get("registry") != expected["registry"]:
    fail(f"registry mismatch: got {actual.get('registry')!r}")

if actual.get("quarantined") != expected["quarantined"]:
    fail(f"quarantined mismatch.\n expected: {expected['quarantined']}\n got     : {actual.get('quarantined')}")

exp_pkgs = expected["packages"]
act_pkgs = actual.get("packages")
if not isinstance(act_pkgs, list):
    fail("packages is not a list")
if len(act_pkgs) != len(exp_pkgs):
    fail(f"packages length mismatch: expected {len(exp_pkgs)}, got {len(act_pkgs)}")

for i, (ep, ap) in enumerate(zip(exp_pkgs, act_pkgs)):
    if not isinstance(ap, dict):
        fail(f"packages[{i}] is not an object")
    for key in ("name", "latest", "ordered", "count"):
        if ap.get(key) != ep[key]:
            fail(f"packages[{i}] ({ep['name']}) field {key!r} mismatch.\n expected: {ep[key]}\n got     : {ap.get(key)}")

print("PASS")
with open(REWARD, "w") as f:
    f.write("1")
PYEOF
