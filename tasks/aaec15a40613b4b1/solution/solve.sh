#!/bin/bash
set -euo pipefail

LAB=/home/user/jar_lab
BUILD="$LAB/build"
DIST="$LAB/dist"
JAR="$DIST/diag-probe-1.2.0.jar"

rm -rf "$BUILD"
mkdir -p "$BUILD/classes" "$BUILD/classes/META-INF/versions/11" "$DIST"

javac --release 8 -d "$BUILD/classes" \
  "$LAB/src/base/acme/diag/Main.java" \
  "$LAB/src/base/acme/diag/VersionProbe.java"

javac --release 11 -d "$BUILD/classes/META-INF/versions/11" \
  "$LAB/src/java11/acme/diag/VersionProbe.java"

python3 - <<'PY'
from pathlib import Path
import zipfile

lab = Path("/home/user/jar_lab")
classes = lab / "build" / "classes"
jar_path = lab / "dist" / "diag-probe-1.2.0.jar"

manifest = (
    b"Manifest-Version: 1.0\r\n"
    b"Main-Class: acme.diag.Main\r\n"
    b"Multi-Release: true\r\n"
    b"Created-By: terminal-rsi\r\n"
    b"\r\n"
)

entries = [
    ("META-INF/", None, 0o40755),
    ("META-INF/MANIFEST.MF", manifest, 0o100644),
    ("acme/", None, 0o40755),
    ("acme/diag/", None, 0o40755),
    ("acme/diag/Main.class", classes / "acme/diag/Main.class", 0o100644),
    ("acme/diag/VersionProbe.class", classes / "acme/diag/VersionProbe.class", 0o100644),
    ("META-INF/versions/", None, 0o40755),
    ("META-INF/versions/11/", None, 0o40755),
    ("META-INF/versions/11/acme/", None, 0o40755),
    ("META-INF/versions/11/acme/diag/", None, 0o40755),
    ("META-INF/versions/11/acme/diag/VersionProbe.class", classes / "META-INF/versions/11/acme/diag/VersionProbe.class", 0o100644),
]

with zipfile.ZipFile(jar_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, source, mode in entries:
        info = zipfile.ZipInfo(name, (2024, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = mode << 16
        data = b"" if source is None else (source if isinstance(source, bytes) else source.read_bytes())
        zf.writestr(info, data)
PY

java -jar "$JAR" >/tmp/diag-probe.out
grep -qx 'diag-probe 1.2.0: java11-runtime' /tmp/diag-probe.out
