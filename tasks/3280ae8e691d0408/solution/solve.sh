#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import hashlib
import shutil
import stat
import zipfile
from pathlib import Path

root = Path("/app")
staging = root / "staging"
artifact_root = root / "maven-repo" / "com" / "acme" / "telemetry-core"
version_dir = artifact_root / "2.7.1"

if artifact_root.exists():
    for child in artifact_root.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
version_dir.mkdir(parents=True, exist_ok=True)

manifest = (
    "Manifest-Version: 1.0\n"
    "Created-By: terminal-rsi\n"
    "Implementation-Title: telemetry-core\n"
    "Implementation-Version: 2.7.1\n"
    "\n"
).encode("utf-8")

entries = [
    ("META-INF/MANIFEST.MF", manifest),
    ("com/acme/telemetry/Collector.class", (staging / "classes/com/acme/telemetry/Collector.class").read_bytes()),
    ("com/acme/telemetry/internal/Envelope.class", (staging / "classes/com/acme/telemetry/internal/Envelope.class").read_bytes()),
    ("META-INF/services/com.acme.telemetry.Plugin", (staging / "classes/META-INF/services/com.acme.telemetry.Plugin").read_bytes()),
]

jar_path = version_dir / "telemetry-core-2.7.1.jar"
with zipfile.ZipFile(jar_path, "w") as zf:
    for name, data in entries:
        info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.create_system = 3
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        zf.writestr(info, data)

pom_path = version_dir / "telemetry-core-2.7.1.pom"
pom_path.write_bytes((staging / "pom.xml").read_bytes())

metadata_path = artifact_root / "maven-metadata.xml"
metadata_path.write_text(
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
    "</metadata>\n",
    encoding="utf-8",
)

for path in [jar_path, pom_path, metadata_path]:
    data = path.read_bytes()
    for suffix, algo in [(".md5", "md5"), (".sha1", "sha1"), (".sha256", "sha256")]:
        digest = hashlib.new(algo, data).hexdigest()
        path.with_name(path.name + suffix).write_text(digest + "\n", encoding="ascii")
PY
