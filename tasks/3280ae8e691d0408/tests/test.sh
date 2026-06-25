#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import shutil
import stat
import sys
import tempfile
import zipfile
from pathlib import Path

root = Path("/app")
staging = root / "staging"
artifact_root = root / "maven-repo" / "com" / "acme" / "telemetry-core"
version_dir = artifact_root / "2.7.1"
version = "2.7.1"
base = f"telemetry-core-{version}"

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        fail(f"missing required file: {path}")

expected_artifact_entries = ["2.7.1", "maven-metadata.xml", "maven-metadata.xml.md5", "maven-metadata.xml.sha1", "maven-metadata.xml.sha256"]
if sorted(p.name for p in artifact_root.iterdir()) != expected_artifact_entries:
    fail("artifact directory has missing, stale, or extra entries")

expected_version_entries = sorted([
    f"{base}.jar",
    f"{base}.jar.md5",
    f"{base}.jar.sha1",
    f"{base}.jar.sha256",
    f"{base}.pom",
    f"{base}.pom.md5",
    f"{base}.pom.sha1",
    f"{base}.pom.sha256",
])
if sorted(p.name for p in version_dir.iterdir()) != expected_version_entries:
    fail("version directory has missing, stale, or extra entries")

metadata = (
    "<metadata>\n"
    "  <groupId>com.acme</groupId>\n"
    "  <artifactId>telemetry-core</artifactId>\n"
    "  <versioning>\n"
    "    <release>2.7.1</release>\n"
    "    <versions>\n"
    "      <version>2.7.1</version>\n"
    "    </versions>\n"
    "    <lastUpdated>20260625000000</lastUpdated>\n"
    "  </versioning>\n"
    "</metadata>\n"
).encode("utf-8")
if read_bytes(artifact_root / "maven-metadata.xml") != metadata:
    fail("maven-metadata.xml content, indentation, timestamp, or trailing newline is incorrect")

pom_bytes = read_bytes(staging / "pom.xml")
if read_bytes(version_dir / f"{base}.pom") != pom_bytes:
    fail("POM was not copied byte-for-byte from /app/staging/pom.xml")

manifest = (
    "Manifest-Version: 1.0\n"
    "Created-By: terminal-rsi\n"
    "Implementation-Title: telemetry-core\n"
    "Implementation-Version: 2.7.1\n"
    "\n"
).encode("utf-8")
expected_members = [
    "META-INF/MANIFEST.MF",
    "com/acme/telemetry/Collector.class",
    "com/acme/telemetry/internal/Envelope.class",
    "META-INF/services/com.acme.telemetry.Plugin",
]

with tempfile.TemporaryDirectory() as td:
    expected_jar = Path(td) / "expected.jar"
    with zipfile.ZipFile(expected_jar, "w") as zf:
        for name, data in [
            (expected_members[0], manifest),
            (expected_members[1], read_bytes(staging / "classes/com/acme/telemetry/Collector.class")),
            (expected_members[2], read_bytes(staging / "classes/com/acme/telemetry/internal/Envelope.class")),
            (expected_members[3], read_bytes(staging / "classes/META-INF/services/com.acme.telemetry.Plugin")),
        ]:
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            zf.writestr(info, data)

    jar_path = version_dir / f"{base}.jar"
    jar_bytes = read_bytes(jar_path)
    if jar_bytes != expected_jar.read_bytes():
        fail("JAR bytes are not the required deterministic ZIP artifact")

try:
    with zipfile.ZipFile(version_dir / f"{base}.jar") as zf:
        infos = zf.infolist()
        if [info.filename for info in infos] != expected_members:
            fail("JAR member set or order is incorrect")
        for info in infos:
            if info.date_time != (1980, 1, 1, 0, 0, 0):
                fail(f"{info.filename} has a non-normalized ZIP timestamp")
            if info.create_system != 3:
                fail(f"{info.filename} was not written with Unix ZIP metadata")
            mode = (info.external_attr >> 16) & 0o777
            if mode != 0o644:
                fail(f"{info.filename} mode is {oct(mode)}, expected 0o644")
        if zf.read("META-INF/MANIFEST.MF") != manifest:
            fail("JAR manifest content is incorrect")
except zipfile.BadZipFile:
    fail("JAR is not a valid ZIP archive")

for path in [
    version_dir / f"{base}.jar",
    version_dir / f"{base}.pom",
    artifact_root / "maven-metadata.xml",
]:
    data = read_bytes(path)
    expected = {
        ".md5": hashlib.md5(data).hexdigest(),
        ".sha1": hashlib.sha1(data).hexdigest(),
        ".sha256": hashlib.sha256(data).hexdigest(),
    }
    for suffix, digest in expected.items():
        sidecar = path.with_name(path.name + suffix)
        if read_bytes(sidecar) != (digest + "\n").encode("ascii"):
            fail(f"{sidecar.name} has the wrong digest, algorithm, case, or trailing newline")

print("ok")
PY

if [ "$?" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
