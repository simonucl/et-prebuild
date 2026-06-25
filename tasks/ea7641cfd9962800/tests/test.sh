#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import io
import stat
import sys
import zipfile
from pathlib import Path

src = Path("/app/maven-src")
base = Path("/app/repo/com/acme/edge-policy-runtime")
version_dir = base / "2.4.1"

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        fail(f"missing required file: {path}")

def digest(data: bytes, algo: str) -> str:
    return hashlib.new(algo, data).hexdigest()

expected_base_files = {
    "2.4.1",
    "maven-metadata.xml",
    "maven-metadata.xml.md5",
    "maven-metadata.xml.sha1",
    "maven-metadata.xml.sha256",
}
if {p.name for p in base.iterdir()} != expected_base_files:
    fail("repository base contains stale, missing, or unexpected entries")

expected_version_files = {
    "edge-policy-runtime-2.4.1.jar",
    "edge-policy-runtime-2.4.1.jar.md5",
    "edge-policy-runtime-2.4.1.jar.sha1",
    "edge-policy-runtime-2.4.1.jar.sha256",
    "edge-policy-runtime-2.4.1.pom",
    "edge-policy-runtime-2.4.1.pom.md5",
    "edge-policy-runtime-2.4.1.pom.sha1",
    "edge-policy-runtime-2.4.1.pom.sha256",
}
if {p.name for p in version_dir.iterdir() if p.is_file()} != expected_version_files:
    fail("version directory contains stale, missing, or unexpected files")

manifest = (
    "Manifest-Version: 1.0\r\n"
    "Implementation-Title: edge-policy-runtime\r\n"
    "Implementation-Version: 2.4.1\r\n"
    "Built-By: terminal-rsi\r\n"
    "\r\n"
).encode("utf-8")
members = [
    ("META-INF/MANIFEST.MF", manifest),
    ("com/acme/edgepolicy/Runtime.class", read_bytes(src / "classes/com/acme/edgepolicy/Runtime.class")),
    ("com/acme/edgepolicy/schema.json", read_bytes(src / "resources/com/acme/edgepolicy/schema.json")),
    ("LICENSE.txt", read_bytes(src / "LICENSE.txt")),
]

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, data in members:
        info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.create_system = 3
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        zf.writestr(info, data)
expected_jar = buf.getvalue()
actual_jar = read_bytes(version_dir / "edge-policy-runtime-2.4.1.jar")
if actual_jar != expected_jar:
    try:
        with zipfile.ZipFile(io.BytesIO(actual_jar)) as zf:
            names = zf.namelist()
            if names != [name for name, _ in members]:
                fail(f"JAR has wrong members or order: {names}")
            for info in zf.infolist():
                if info.is_dir():
                    fail("JAR must not contain directory entries")
                if info.date_time != (1980, 1, 1, 0, 0, 0):
                    fail(f"{info.filename} timestamp is not normalized")
                if info.create_system != 3:
                    fail(f"{info.filename} does not store Unix metadata")
                mode = (info.external_attr >> 16) & 0o777
                if mode != 0o644:
                    fail(f"{info.filename} mode is {oct(mode)}, expected 0o644")
    except zipfile.BadZipFile:
        fail("JAR is not a valid ZIP archive")
    fail("JAR bytes are not the required deterministic package")

expected_pom = b'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.acme</groupId>
  <artifactId>edge-policy-runtime</artifactId>
  <version>2.4.1</version>
  <packaging>jar</packaging>
  <name>Acme Edge Policy Runtime</name>
  <licenses>
    <license>
      <name>Apache-2.0</name>
    </license>
  </licenses>
</project>
'''
if read_bytes(version_dir / "edge-policy-runtime-2.4.1.pom") != expected_pom:
    fail("POM content is not the required Maven artifact descriptor")

expected_metadata = b'''<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <groupId>com.acme</groupId>
  <artifactId>edge-policy-runtime</artifactId>
  <versioning>
    <latest>2.4.1</latest>
    <release>2.4.1</release>
    <versions>
      <version>2.4.1</version>
    </versions>
    <lastUpdated>20260625000000</lastUpdated>
  </versioning>
</metadata>
'''
if read_bytes(base / "maven-metadata.xml") != expected_metadata:
    fail("maven-metadata.xml content is incorrect")

for path in [
    version_dir / "edge-policy-runtime-2.4.1.jar",
    version_dir / "edge-policy-runtime-2.4.1.pom",
    base / "maven-metadata.xml",
]:
    data = path.read_bytes()
    for suffix, algo in [(".md5", "md5"), (".sha1", "sha1"), (".sha256", "sha256")]:
        expected = digest(data, algo) + "\n"
        if read_bytes(path.with_name(path.name + suffix)).decode("ascii") != expected:
            fail(f"{path.name}{suffix} checksum is wrong or missing its single trailing newline")

print("Maven repository validated")
PY

if [ "$?" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
