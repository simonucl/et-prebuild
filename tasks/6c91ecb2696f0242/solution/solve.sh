#!/bin/bash
set -euo pipefail

SRC=/home/user/jar_lab/src
DIST=/home/user/jar_lab/dist
BUILD=/home/user/jar_lab/build

rm -rf "$BUILD"
mkdir -p "$BUILD/classes" "$DIST"
find "$DIST" -mindepth 1 -maxdepth 1 -exec rm -rf {} +

javac -encoding UTF-8 -d "$BUILD/classes" \
  "$SRC/com/acme/scrub/Scrubber.java" \
  "$SRC/com/acme/scrub/Redactor.java" \
  "$SRC/com/acme/scrub/Main.java"

python3 - <<'PY'
import hashlib
import shutil
import zipfile
from pathlib import Path

src = Path("/home/user/jar_lab/src")
build = Path("/home/user/jar_lab/build/classes")
dist = Path("/home/user/jar_lab/dist")
jar_path = dist / "log-scrubber-1.2.0.jar"
pom_path = dist / "log-scrubber-1.2.0.pom"

manifest = (
    "Manifest-Version: 1.0\n"
    "Main-Class: com.acme.scrub.Main\n"
    "Implementation-Title: log-scrubber\n"
    "Implementation-Version: 1.2.0\n"
    "Built-By: terminal-rsi\n"
    "Created-By: terminal-rsi\n"
    "\n"
).encode("utf-8")

members = [
    ("META-INF/MANIFEST.MF", manifest),
    ("META-INF/services/com.acme.scrub.Scrubber", (src / "META-INF/services/com.acme.scrub.Scrubber").read_bytes()),
    ("com/acme/scrub/Main.class", (build / "com/acme/scrub/Main.class").read_bytes()),
    ("com/acme/scrub/Redactor.class", (build / "com/acme/scrub/Redactor.class").read_bytes()),
    ("com/acme/scrub/Scrubber.class", (build / "com/acme/scrub/Scrubber.class").read_bytes()),
    ("com/acme/scrub/rules/default-rules.txt", (src / "com/acme/scrub/rules/default-rules.txt").read_bytes()),
]

with zipfile.ZipFile(jar_path, "w") as zf:
    for name, data in members:
        info = zipfile.ZipInfo(name, (2024, 5, 6, 7, 8, 10))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.create_system = 3
        info.external_attr = 0o100644 << 16
        zf.writestr(info, data)

pom = """<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd\">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.acme</groupId>
  <artifactId>log-scrubber</artifactId>
  <version>1.2.0</version>
  <name>log-scrubber</name>
  <description>Offline log redaction utility</description>
</project>
"""
pom_path.write_text(pom, encoding="utf-8")

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

(dist / "SHA256SUMS").write_text(
    f"{sha256(jar_path)}  log-scrubber-1.2.0.jar\n"
    f"{sha256(pom_path)}  log-scrubber-1.2.0.pom\n",
    encoding="utf-8",
)

shutil.rmtree("/home/user/jar_lab/build")
PY
