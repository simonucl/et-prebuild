#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import hashlib
import stat
import zipfile
from pathlib import Path

src = Path("/app/maven-src")
base = Path("/app/repo/com/acme/edge-policy-runtime")
version = "2.4.1"
version_dir = base / version
version_dir.mkdir(parents=True, exist_ok=True)

for child in list(base.iterdir()):
    if child.name not in {version, "maven-metadata.xml", "maven-metadata.xml.md5", "maven-metadata.xml.sha1", "maven-metadata.xml.sha256"}:
        if child.is_dir():
            import shutil
            shutil.rmtree(child)
        else:
            child.unlink()

for child in list(version_dir.iterdir()):
    child.unlink()

fixed_time = (1980, 1, 1, 0, 0, 0)
manifest = (
    "Manifest-Version: 1.0\r\n"
    "Implementation-Title: edge-policy-runtime\r\n"
    "Implementation-Version: 2.4.1\r\n"
    "Built-By: terminal-rsi\r\n"
    "\r\n"
).encode("utf-8")

jar_members = [
    ("META-INF/MANIFEST.MF", manifest),
    ("com/acme/edgepolicy/Runtime.class", (src / "classes/com/acme/edgepolicy/Runtime.class").read_bytes()),
    ("com/acme/edgepolicy/schema.json", (src / "resources/com/acme/edgepolicy/schema.json").read_bytes()),
    ("LICENSE.txt", (src / "LICENSE.txt").read_bytes()),
]

jar_path = version_dir / "edge-policy-runtime-2.4.1.jar"
with zipfile.ZipFile(jar_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, data in jar_members:
        info = zipfile.ZipInfo(name, fixed_time)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.create_system = 3
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        zf.writestr(info, data)

pom = """<?xml version="1.0" encoding="UTF-8"?>
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
"""
(version_dir / "edge-policy-runtime-2.4.1.pom").write_text(pom, encoding="utf-8")

metadata = """<?xml version="1.0" encoding="UTF-8"?>
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
"""
(base / "maven-metadata.xml").write_text(metadata, encoding="utf-8")

def write_sums(path: Path) -> None:
    data = path.read_bytes()
    for suffix, algo in [(".md5", "md5"), (".sha1", "sha1"), (".sha256", "sha256")]:
        digest = hashlib.new(algo, data).hexdigest()
        (path.with_name(path.name + suffix)).write_text(digest + "\n", encoding="ascii")

write_sums(jar_path)
write_sums(version_dir / "edge-policy-runtime-2.4.1.pom")
write_sums(base / "maven-metadata.xml")
PY
