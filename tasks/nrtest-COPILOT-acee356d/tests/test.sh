#!/bin/bash
# Deterministic verifier: recomputes the correct plan from /home/user/registry and
# compares it byte-for-byte against the agent's output (generated_at value is a wildcard).
mkdir -p /logs/verifier

python3 - <<'PYEOF'
import os, json, glob, re, sys

REG = "/home/user/registry"
JSON_PATH = "/home/user/reports/upgrade_plan.json"
LOG_PATH = "/home/user/reports/upgrade_plan.log"

def fail(msg):
    sys.stderr.write("VERIFIER FAIL: " + msg + "\n")
    with open("/logs/verifier/reward.txt", "w") as f:
        f.write("0\n")
    sys.exit(0)

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

# --- Recompute expected plan from source of truth ---
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
log_lines = []
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
    })
    log_lines.append(f"{name} keep {latest} reclaim {reclaimable} bytes from {len(reclaim_entries)} artefact(s)")
log_lines.append(f"TOTAL reclaimable {total} bytes")

GEN = "@@GENERATED_AT@@"
expected_doc = {
    "registry": REG,
    "generated_at": GEN,
    "packages": packages,
    "total_reclaimable_bytes": total,
}
expected_json = json.dumps(expected_doc, separators=(",", ":")) + "\n"
expected_log = "\n".join(log_lines) + "\n"

# --- Check reports dir permissions ---
rep = "/home/user/reports"
if not os.path.isdir(rep):
    fail("/home/user/reports does not exist")
mode = oct(os.stat(rep).st_mode & 0o777)
if (os.stat(rep).st_mode & 0o755) != 0o755:
    fail(f"/home/user/reports must be at least mode 755, got {mode}")

# --- Validate JSON file ---
if not os.path.isfile(JSON_PATH):
    fail("upgrade_plan.json missing")
with open(JSON_PATH, "rb") as f:
    raw = f.read()
try:
    text = raw.decode("utf-8")
except Exception as e:
    fail(f"json not utf-8: {e}")

# It must parse and generated_at must be a valid RFC-3339 UTC timestamp.
try:
    parsed = json.loads(text)
except Exception as e:
    fail(f"json does not parse: {e}")
ga = parsed.get("generated_at")
if not isinstance(ga, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", ga):
    fail(f"generated_at not RFC-3339 UTC 'YYYY-MM-DDThh:mm:ssZ': {ga!r}")

# Normalise the agent's generated_at value, then require byte-exact minified match.
# Replace only the first occurrence of the generated_at string value.
normalized = text.replace(f'"generated_at":"{ga}"', f'"generated_at":"{GEN}"', 1)
if normalized != expected_json:
    # Provide a focused diff hint.
    sys.stderr.write("---EXPECTED (generated_at masked)---\n" + expected_json + "\n")
    sys.stderr.write("---GOT (generated_at masked)---\n" + normalized + "\n")
    fail("upgrade_plan.json does not match expected minified/ordered content")

# --- Validate LOG file ---
if not os.path.isfile(LOG_PATH):
    fail("upgrade_plan.log missing")
with open(LOG_PATH, "rb") as f:
    got_log = f.read().decode("utf-8")
if got_log != expected_log:
    sys.stderr.write("---EXPECTED LOG---\n" + expected_log + "\n")
    sys.stderr.write("---GOT LOG---\n" + got_log + "\n")
    fail("upgrade_plan.log does not match expected content")

with open("/logs/verifier/reward.txt", "w") as f:
    f.write("1\n")
print("VERIFIER PASS")
PYEOF
