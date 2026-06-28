#!/bin/bash
set -e

WORK=/home/user/work
mkdir -p "$WORK/out"

python3 - "$WORK" <<'PY'
import json, os, sys
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet

work = sys.argv[1]

def load_specs(path):
    specs = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            parts = s.split(None, 1)
            name = parts[0]
            spec = parts[1].strip() if len(parts) > 1 else ""
            specs.append((name, spec))
    return specs

specs = load_specs(os.path.join(work, "packages.txt"))
packages = []
tot_valid = tot_invalid = resolved = 0

for name, spec in sorted(specs, key=lambda x: x[0]):
    ss = SpecifierSet(spec)
    valid = []
    invalid = []
    with open(os.path.join(work, "candidates", name + ".txt")) as f:
        for raw in f:
            s = raw.strip()
            if s == "":
                continue
            try:
                valid.append(Version(s))
            except InvalidVersion:
                invalid.append(s)
    valid_sorted = sorted(valid)               # stable sort keeps input order on ties
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

out = {
    "tool": "pep440-resolver/v1",
    "packages": packages,
    "summary": {
        "packages": len(packages),
        "valid": tot_valid,
        "invalid": tot_invalid,
        "resolved": resolved,
    },
}

with open(os.path.join(work, "out", "resolution.json"), "w") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
PY

echo "oracle: wrote $WORK/out/resolution.json"
