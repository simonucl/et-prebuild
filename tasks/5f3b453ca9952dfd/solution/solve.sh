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
repo = root / "repo" / "com" / "acme" / "telemetry-agent"
version_dir = repo / "2.4.1"
version_dir.mkdir(parents=True, exist_ok=True)

for path in list(repo.rglob("*")):
    if path.is_file():
        path.unlink()
for path in sorted([p for p in repo.rglob("*") if p.is_dir() and p != version_dir and p != repo], reverse=True):
    try:
        path.rmdir()
    except OSError:
        pass
version_dir.mkdir(parents=True, exist_ok=True)

fixed = (1980, 1, 1, 0, 0, 0)
manifest = b"Manifest-Version: 1.0\r\nCreated-By: terminal-rsi\r\nBuild-Jdk-Spec: 17\r\n\r\n"

def add_dir(zf: zipfile.ZipFile, name: str) -> None:
    info = zipfile.ZipInfo(name, fixed)
    info.create_system = 3
    info.external_attr = (stat.S_IFDIR | 0o755) << 16
    zf.writestr(info, b"")

def add_file(zf: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, fixed)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | 0o644) << 16
    zf.writestr(info, data)

with zipfile.ZipFile(version_dir / "telemetry-agent-2.4.1.jar", "w") as zf:
    add_dir(zf, "META-INF/")
    add_file(zf, "META-INF/MANIFEST.MF", manifest)
    add_dir(zf, "META-INF/services/")
    add_file(zf, "META-INF/services/com.acme.telemetry.Plugin", (staging / "resources/META-INF/services/com.acme.telemetry.Plugin").read_bytes())
    add_dir(zf, "com/")
    add_dir(zf, "com/acme/")
    add_dir(zf, "com/acme/telemetry/")
    add_file(zf, "com/acme/telemetry/Agent.class", (staging / "classes/com/acme/telemetry/Agent.class").read_bytes())
    add_dir(zf, "com/acme/telemetry/internal/")
    add_file(zf, "com/acme/telemetry/internal/Config.class", (staging / "classes/com/acme/telemetry/internal/Config.class").read_bytes())
    add_file(zf, "LICENSE.txt", (staging / "LICENSE.txt").read_bytes())

with zipfile.ZipFile(version_dir / "telemetry-agent-2.4.1-sources.jar", "w") as zf:
    add_dir(zf, "META-INF/")
    add_file(zf, "META-INF/MANIFEST.MF", manifest)
    add_dir(zf, "com/")
    add_dir(zf, "com/acme/")
    add_dir(zf, "com/acme/telemetry/")
    add_file(zf, "com/acme/telemetry/Agent.java", (staging / "sources/com/acme/telemetry/Agent.java").read_bytes())
    add_dir(zf, "com/acme/telemetry/internal/")
    add_file(zf, "com/acme/telemetry/internal/Config.java", (staging / "sources/com/acme/telemetry/internal/Config.java").read_bytes())
    add_file(zf, "LICENSE.txt", (staging / "LICENSE.txt").read_bytes())

shutil.copyfile(staging / "pom.xml", version_dir / "telemetry-agent-2.4.1.pom")

(repo / "maven-metadata.xml").write_text(
    "<metadata>\n"
    "  <groupId>com.acme</groupId>\n"
    "  <artifactId>telemetry-agent</artifactId>\n"
    "  <versioning>\n"
    "    <release>2.4.1</release>\n"
    "    <versions>\n"
    "      <version>2.4.1</version>\n"
    "    </versions>\n"
    "    <lastUpdated>20260102030405</lastUpdated>\n"
    "  </versioning>\n"
    "</metadata>\n",
    encoding="utf-8",
)

for path in [
    version_dir / "telemetry-agent-2.4.1.jar",
    version_dir / "telemetry-agent-2.4.1-sources.jar",
    version_dir / "telemetry-agent-2.4.1.pom",
    repo / "maven-metadata.xml",
]:
    data = path.read_bytes()
    (path.with_name(path.name + ".sha1")).write_text(hashlib.sha1(data).hexdigest() + "\n", encoding="ascii")
    (path.with_name(path.name + ".md5")).write_text(hashlib.md5(data).hexdigest() + "\n", encoding="ascii")
PY
