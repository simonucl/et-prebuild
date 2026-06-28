#!/bin/bash
set -e

python3 - <<'PYEOF'
import os, re, json, functools

ARTDIR = "/home/user/registry/artifacts"
OUT = "/home/user/report.json"

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
            return -c  # descending precedence
        if v1 < v2: return -1
        if v1 > v2: return 1
        return 0
    return sorted(versions, key=functools.cmp_to_key(comparator))

valid = {}      # name -> [version strings]
quarantined = []
for fn in os.listdir(ARTDIR):
    if not fn.endswith('.bin'):
        continue
    stem = fn[:-4]            # strip .bin
    name, _, ver = stem.partition('@')
    if '@' not in stem:
        continue
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

report = {
    "registry": ARTDIR,
    "packages": packages,
    "quarantined": sorted(quarantined),
}

with open(OUT, 'w') as f:
    json.dump(report, f, indent=2)
PYEOF

echo "wrote /home/user/report.json"
