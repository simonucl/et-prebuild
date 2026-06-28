#!/bin/bash
# Deterministic verifier. Independently recomputes the expected curation from the
# read-only feed using dpkg, then compares the agent's two output files byte-for-byte.
# Writes 0/1 to /logs/verifier/reward.txt.
mkdir -p /logs/verifier

python3 - <<'PY'
import json, subprocess, functools, os

SRC = "/home/user/pool/versions.txt"
OUT = "/home/user/out"
REWARD = "/logs/verifier/reward.txt"

def fail(msg):
    print("FAIL:", msg)
    with open(REWARD, "w") as f:
        f.write("0")
    raise SystemExit(0)

def dctl(a, op, b):
    return subprocess.run(["dpkg", "--compare-versions", a, op, b]).returncode == 0

def vcmp(a, b):
    if dctl(a, "lt", b):
        return -1
    if dctl(a, "gt", b):
        return 1
    return 0

vkey = functools.cmp_to_key(vcmp)

# ---- recompute expected ----
pkgs = {}
with open(SRC) as f:
    for raw in f:
        line = raw.rstrip("\n")
        s = line.lstrip()
        if s == "" or s.startswith("#"):
            continue
        name, version = line.split(" ", 1)
        pkgs.setdefault(name.strip(), set()).add(version.strip())

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
expected_manifest = json.dumps(manifest, separators=(",", ":")) + "\n"
expected_latest = "".join("%s %s\n" % (p["name"], p["latest"]) for p in packages)

# ---- checks ----
if not os.path.isdir(OUT):
    fail("/home/user/out does not exist")

mpath = os.path.join(OUT, "manifest.json")
if not os.path.isfile(mpath):
    fail("manifest.json missing")
actual_manifest = open(mpath).read()
if actual_manifest != expected_manifest:
    print("---expected manifest.json---"); print(repr(expected_manifest))
    print("---actual manifest.json---"); print(repr(actual_manifest))
    fail("manifest.json does not match (content / key-order / ordering / minification / newline)")

lpath = os.path.join(OUT, "latest.txt")
if not os.path.isfile(lpath):
    fail("latest.txt missing")
actual_latest = open(lpath).read()
if actual_latest != expected_latest:
    print("---expected latest.txt---"); print(repr(expected_latest))
    print("---actual latest.txt---"); print(repr(actual_latest))
    fail("latest.txt does not match expected")

with open(REWARD, "w") as f:
    f.write("1")
print("PASS")
PY

# safety net: if python crashed before writing a reward, record 0
if [ ! -s /logs/verifier/reward.txt ]; then
  echo 0 > /logs/verifier/reward.txt
fi
