#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier
REWARD=0

fail() {
  echo "$1"
  echo 0 > /logs/verifier/reward.txt
  exit 0
}

DIST=/home/user/jar_lab/dist
SRC=/home/user/jar_lab/src
JAR="$DIST/log-scrubber-1.2.0.jar"
POM="$DIST/log-scrubber-1.2.0.pom"
SUMS="$DIST/SHA256SUMS"

[ -d "$DIST" ] || fail "dist directory is missing"

mapfile -t entries < <(cd "$DIST" && find . -mindepth 1 -maxdepth 1 -printf '%f\n' | LC_ALL=C sort)
expected_dist=("SHA256SUMS" "log-scrubber-1.2.0.jar" "log-scrubber-1.2.0.pom")
if [ "${entries[*]}" != "${expected_dist[*]}" ]; then
  fail "dist contains unexpected entries: ${entries[*]}"
fi

[ -f "$JAR" ] || fail "missing jar"
[ -f "$POM" ] || fail "missing pom"
[ -f "$SUMS" ] || fail "missing SHA256SUMS"

python3 - <<'PY' || fail "jar, pom, checksum, or runtime validation failed"
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

dist = Path("/home/user/jar_lab/dist")
src = Path("/home/user/jar_lab/src")
jar = dist / "log-scrubber-1.2.0.jar"
pom = dist / "log-scrubber-1.2.0.pom"
sums = dist / "SHA256SUMS"

expected_members = [
    "META-INF/MANIFEST.MF",
    "META-INF/services/com.acme.scrub.Scrubber",
    "com/acme/scrub/Main.class",
    "com/acme/scrub/Redactor.class",
    "com/acme/scrub/Scrubber.class",
    "com/acme/scrub/rules/default-rules.txt",
]

manifest = (
    "Manifest-Version: 1.0\n"
    "Main-Class: com.acme.scrub.Main\n"
    "Implementation-Title: log-scrubber\n"
    "Implementation-Version: 1.2.0\n"
    "Built-By: terminal-rsi\n"
    "Created-By: terminal-rsi\n"
    "\n"
).encode()

with zipfile.ZipFile(jar, "r") as zf:
    infos = zf.infolist()
    names = [info.filename for info in infos]
    if names != expected_members:
        raise SystemExit(f"unexpected jar members or order: {names}")
    for info in infos:
        if info.is_dir():
            raise SystemExit("jar must not contain directory entries")
        if info.compress_type != zipfile.ZIP_DEFLATED:
            raise SystemExit(f"{info.filename} is not deflated")
        if info.date_time != (2024, 5, 6, 7, 8, 10):
            raise SystemExit(f"{info.filename} has wrong timestamp {info.date_time}")
        if (info.external_attr >> 16) & 0o777 != 0o644:
            raise SystemExit(f"{info.filename} has wrong zip permission")
    if zf.read("META-INF/MANIFEST.MF") != manifest:
        raise SystemExit("manifest content is incorrect")
    if zf.read("META-INF/services/com.acme.scrub.Scrubber") != (src / "META-INF/services/com.acme.scrub.Scrubber").read_bytes():
        raise SystemExit("service provider file content is incorrect")
    if zf.read("com/acme/scrub/rules/default-rules.txt") != (src / "com/acme/scrub/rules/default-rules.txt").read_bytes():
        raise SystemExit("default rules resource content is incorrect")
    for name in names:
        if name.endswith(".java"):
            raise SystemExit("jar includes Java source")

expected_pom = """<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd\">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.acme</groupId>
  <artifactId>log-scrubber</artifactId>
  <version>1.2.0</version>
  <name>log-scrubber</name>
  <description>Offline log redaction utility</description>
</project>
"""
if pom.read_text(encoding="utf-8") != expected_pom:
    raise SystemExit("pom content is incorrect")

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected_sums = (
    f"{sha256(jar)}  log-scrubber-1.2.0.jar\n"
    f"{sha256(pom)}  log-scrubber-1.2.0.pom\n"
)
if sums.read_text(encoding="utf-8") != expected_sums:
    raise SystemExit("SHA256SUMS content is incorrect")

run = subprocess.run(
    ["java", "-jar", str(jar)],
    input="contact alice@example.com token=abcdef123456 API-Key=XYZ987654\n",
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    timeout=10,
)
if run.returncode != 0:
    raise SystemExit(f"java -jar failed: {run.stderr}")
expected_out = "contact [redacted-email] token=[redacted-secret] API-Key=[redacted-secret]\n"
if run.stdout != expected_out:
    raise SystemExit(f"unexpected runtime output: {run.stdout!r}")
PY

echo 1 > /logs/verifier/reward.txt
exit 0
