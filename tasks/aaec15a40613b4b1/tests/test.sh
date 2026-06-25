#!/bin/bash
set -u

mkdir -p /logs/verifier
REWARD=0
JAR=/home/user/jar_lab/dist/diag-probe-1.2.0.jar
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

fail() {
  echo "FAIL: $1"
  echo "$REWARD" > /logs/verifier/reward.txt
  exit 0
}

[ -f "$JAR" ] || fail "missing final JAR"

python3 - <<'PY' "$JAR" > "$TMPDIR/zipcheck.txt" 2>&1 || fail "$(cat "$TMPDIR/zipcheck.txt")"
from pathlib import Path
import sys
import zipfile

jar = Path(sys.argv[1])
expected_names = [
    "META-INF/",
    "META-INF/MANIFEST.MF",
    "acme/",
    "acme/diag/",
    "acme/diag/Main.class",
    "acme/diag/VersionProbe.class",
    "META-INF/versions/",
    "META-INF/versions/11/",
    "META-INF/versions/11/acme/",
    "META-INF/versions/11/acme/diag/",
    "META-INF/versions/11/acme/diag/VersionProbe.class",
]
expected_manifest = (
    b"Manifest-Version: 1.0\r\n"
    b"Main-Class: acme.diag.Main\r\n"
    b"Multi-Release: true\r\n"
    b"Created-By: terminal-rsi\r\n"
    b"\r\n"
)
with zipfile.ZipFile(jar) as zf:
    infos = zf.infolist()
    names = [i.filename for i in infos]
    if names != expected_names:
        raise SystemExit(f"unexpected JAR members or order: {names!r}")
    bad_times = [(i.filename, i.date_time) for i in infos if i.date_time != (2024, 1, 1, 0, 0, 0)]
    if bad_times:
        raise SystemExit(f"non-normalized timestamps: {bad_times!r}")
    if zf.read("META-INF/MANIFEST.MF") != expected_manifest:
        raise SystemExit("manifest bytes are not exact")
    if zf.read("acme/diag/VersionProbe.class") == zf.read("META-INF/versions/11/acme/diag/VersionProbe.class"):
        raise SystemExit("base and Java 11 VersionProbe classes are identical")
print("zip structure ok")
PY

java -jar "$JAR" > "$TMPDIR/run.out" 2> "$TMPDIR/run.err" || fail "java -jar failed: $(cat "$TMPDIR/run.err")"
grep -qx 'diag-probe 1.2.0: java11-runtime' "$TMPDIR/run.out" || fail "unexpected java -jar output: $(cat "$TMPDIR/run.out")"

javap -verbose -classpath "$JAR" acme.diag.Main > "$TMPDIR/main.javap" 2>&1 || fail "javap failed for Main"
javap -verbose -classpath "$JAR" acme.diag.VersionProbe > "$TMPDIR/base.javap" 2>&1 || fail "javap failed for base VersionProbe"
javap -verbose --multi-release 11 -classpath "$JAR" acme.diag.VersionProbe > "$TMPDIR/mr.javap" 2>&1 || fail "javap failed for Java 11 VersionProbe"

grep -q 'major version: 52' "$TMPDIR/main.javap" || fail "Main.class is not Java 8 bytecode"
grep -q 'major version: 52' "$TMPDIR/base.javap" || fail "base VersionProbe.class is not Java 8 bytecode"
grep -q 'major version: 55' "$TMPDIR/mr.javap" || fail "Java 11 VersionProbe.class is not Java 11 bytecode"

REWARD=1
echo "$REWARD" > /logs/verifier/reward.txt
echo "PASS: multi-release JAR is correct"
