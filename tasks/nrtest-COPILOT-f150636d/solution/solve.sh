#!/bin/bash
# Oracle solution. Uses dpkg (the canonical Debian version comparator) to order
# versions, then emits the byte-exact manifest + latest list.
set -e

mkdir -p /home/user/out

python3 - <<'PY'
import json, subprocess, functools, os

SRC = "/home/user/pool/versions.txt"
OUT = "/home/user/out"

def dctl(a, op, b):
    return subprocess.run(["dpkg", "--compare-versions", a, op, b]).returncode == 0

def vcmp(a, b):
    if dctl(a, "lt", b):
        return -1
    if dctl(a, "gt", b):
        return 1
    return 0

vkey = functools.cmp_to_key(vcmp)

pkgs = {}
with open(SRC) as f:
    for raw in f:
        line = raw.rstrip("\n")
        s = line.lstrip()
        if s == "" or s.startswith("#"):
            continue
        name, version = line.split(" ", 1)
        name = name.strip()
        version = version.strip()
        pkgs.setdefault(name, set()).add(version)

packages = []
total_versions = 0
for name in sorted(pkgs.keys()):
    versions = sorted(pkgs[name], key=vkey)
    total_versions += len(versions)
    packages.append({
        "name": name,
        "versions": versions,
        "latest": versions[-1],
        "count": len(versions),
        "superseded": versions[:-1],
    })

manifest = {
    "source": SRC,
    "packages": packages,
    "total_packages": len(packages),
    "total_versions": total_versions,
}

with open(os.path.join(OUT, "manifest.json"), "w") as f:
    f.write(json.dumps(manifest, separators=(",", ":")) + "\n")

with open(os.path.join(OUT, "latest.txt"), "w") as f:
    for p in packages:
        f.write("%s %s\n" % (p["name"], p["latest"]))
PY
