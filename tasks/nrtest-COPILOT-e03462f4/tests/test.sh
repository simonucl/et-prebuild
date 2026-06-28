#!/bin/bash
# Deterministic verifier: independently recomputes the expected resolution from the
# read-only inputs and compares the agent's output byte-for-byte.
set -u
mkdir -p /logs/verifier
REWARD=0

WORK=/home/user/work
OUT="$WORK/out/resolution.json"

python3 - "$WORK" "$OUT" <<'PY'
import json, os, sys
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet

work, out_path = sys.argv[1], sys.argv[2]

def load_specs(path):
    specs = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            parts = s.split(None, 1)
            specs.append((parts[0], parts[1].strip() if len(parts) > 1 else ""))
    return specs

specs = load_specs(os.path.join(work, "packages.txt"))
packages = []
tot_valid = tot_invalid = resolved = 0
for name, spec in sorted(specs, key=lambda x: x[0]):
    ss = SpecifierSet(spec)
    valid, invalid = [], []
    with open(os.path.join(work, "candidates", name + ".txt")) as f:
        for raw in f:
            s = raw.strip()
            if s == "":
                continue
            try:
                valid.append(Version(s))
            except InvalidVersion:
                invalid.append(s)
    valid_sorted = sorted(valid)
    sat = [v for v in valid_sorted if ss.contains(v, prereleases=True)]
    best = str(sat[-1]) if sat else None
    stable = [v for v in sat if not v.is_prerelease]
    best_stable = str(stable[-1]) if stable else None
    if best is not None:
        resolved += 1
    tot_valid += len(valid)
    tot_invalid += len(invalid)
    packages.append({
        "name": name,
        "valid": [str(v) for v in valid_sorted],
        "invalid": invalid,
        "best": best,
        "best_stable": best_stable,
        "count_valid": len(valid),
        "count_invalid": len(invalid),
    })
expected = json.dumps({
    "tool": "pep440-resolver/v1",
    "packages": packages,
    "summary": {"packages": len(packages), "valid": tot_valid,
                "invalid": tot_invalid, "resolved": resolved},
}, separators=(",", ":")) + "\n"

# Inputs must be untouched.
try:
    with open(os.path.join(work, "candidates", "django.txt")) as f:
        head = f.readline().strip()
    if head != "3.0":
        print("FAIL: candidate inputs appear modified"); sys.exit(2)
except Exception as e:
    print("FAIL: cannot read inputs:", e); sys.exit(2)

if not os.path.isfile(out_path):
    print("FAIL: missing", out_path); sys.exit(1)
with open(out_path, "rb") as f:
    got = f.read()
want = expected.encode()
if got == want:
    print("PASS: resolution.json matches expected bytes")
    sys.exit(0)
print("FAIL: resolution.json does not match expected bytes.")
print("--- expected ---")
print(want)
print("--- got ---")
print(got)
sys.exit(1)
PY

if [ $? -eq 0 ]; then
  REWARD=1
fi

echo "$REWARD" > /logs/verifier/reward.txt
echo "reward=$REWARD"
