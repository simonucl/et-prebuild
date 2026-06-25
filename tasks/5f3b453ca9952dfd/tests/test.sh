#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import stat
import sys
import zipfile
from pathlib import Path

root = Path("/app")
staging = root / "staging"
repo = root / "repo" / "com" / "acme" / "telemetry-agent"
version_dir = repo / "2.4.1"

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

expected_repo_files = {
    "maven-metadata.xml",
    "maven-metadata.xml.sha1",
    "maven-metadata.xml.md5",
    "2.4.1/telemetry-agent-2.4.1.jar",
    "2.4.1/telemetry-agent-2.4.1.jar.sha1",
    "2.4.1/telemetry-agent-2.4.1.jar.md5",
    "2.4.1/telemetry-agent-2.4.1-sources.jar",
    "2.4.1/telemetry-agent-2.4.1-sources.jar.sha1",
    "2.4.1/telemetry-agent-2.4.1-sources.jar.md5",
    "2.4.1/telemetry-agent-2.4.1.pom",
    "2.4.1/telemetry-agent-2.4.1.pom.sha1",
    "2.4.1/telemetry-agent-2.4.1.pom.md5",
}
actual_repo_files = {str(p.relative_to(repo)) for p in repo.rglob("*") if p.is_file()}
if actual_repo_files != expected_repo_files:
    fail(f"repository file set is wrong: {sorted(actual_repo_files)}")

metadata = (
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
    "</metadata>\n"
).encode()
if (repo / "maven-metadata.xml").read_bytes() != metadata:
    fail("maven-metadata.xml content is not the required single-version metadata")

if (version_dir / "telemetry-agent-2.4.1.pom").read_bytes() != (staging / "pom.xml").read_bytes():
    fail("POM does not exactly match /app/staging/pom.xml")

manifest = b"Manifest-Version: 1.0\r\nCreated-By: terminal-rsi\r\nBuild-Jdk-Spec: 17\r\n\r\n"

def check_jar(path: Path, expected_entries: list[str], expected_payloads: dict[str, bytes]) -> None:
    try:
        with zipfile.ZipFile(path) as zf:
            infos = zf.infolist()
            names = [info.filename for info in infos]
            if names != expected_entries:
                fail(f"{path.name} has wrong member order or file set: {names}")
            for info in infos:
                if info.date_time != (1980, 1, 1, 0, 0, 0):
                    fail(f"{path.name}:{info.filename} has non-normalized timestamp {info.date_time}")
                if info.create_system != 3:
                    fail(f"{path.name}:{info.filename} was not written with Unix metadata")
                mode = (info.external_attr >> 16) & 0o777
                if info.filename.endswith("/"):
                    if mode != 0o755:
                        fail(f"{path.name}:{info.filename} mode is {oct(mode)}, expected 0o755")
                elif mode != 0o644:
                    fail(f"{path.name}:{info.filename} mode is {oct(mode)}, expected 0o644")
            for name, data in expected_payloads.items():
                if zf.read(name) != data:
                    fail(f"{path.name}:{name} content does not match staging input")
    except zipfile.BadZipFile:
        fail(f"{path.name} is not a valid ZIP/JAR file")

check_jar(
    version_dir / "telemetry-agent-2.4.1.jar",
    [
        "META-INF/",
        "META-INF/MANIFEST.MF",
        "META-INF/services/",
        "META-INF/services/com.acme.telemetry.Plugin",
        "com/",
        "com/acme/",
        "com/acme/telemetry/",
        "com/acme/telemetry/Agent.class",
        "com/acme/telemetry/internal/",
        "com/acme/telemetry/internal/Config.class",
        "LICENSE.txt",
    ],
    {
        "META-INF/MANIFEST.MF": manifest,
        "META-INF/services/com.acme.telemetry.Plugin": (staging / "resources/META-INF/services/com.acme.telemetry.Plugin").read_bytes(),
        "com/acme/telemetry/Agent.class": (staging / "classes/com/acme/telemetry/Agent.class").read_bytes(),
        "com/acme/telemetry/internal/Config.class": (staging / "classes/com/acme/telemetry/internal/Config.class").read_bytes(),
        "LICENSE.txt": (staging / "LICENSE.txt").read_bytes(),
    },
)

check_jar(
    version_dir / "telemetry-agent-2.4.1-sources.jar",
    [
        "META-INF/",
        "META-INF/MANIFEST.MF",
        "com/",
        "com/acme/",
        "com/acme/telemetry/",
        "com/acme/telemetry/Agent.java",
        "com/acme/telemetry/internal/",
        "com/acme/telemetry/internal/Config.java",
        "LICENSE.txt",
    ],
    {
        "META-INF/MANIFEST.MF": manifest,
        "com/acme/telemetry/Agent.java": (staging / "sources/com/acme/telemetry/Agent.java").read_bytes(),
        "com/acme/telemetry/internal/Config.java": (staging / "sources/com/acme/telemetry/internal/Config.java").read_bytes(),
        "LICENSE.txt": (staging / "LICENSE.txt").read_bytes(),
    },
)

for artifact in [
    repo / "maven-metadata.xml",
    version_dir / "telemetry-agent-2.4.1.jar",
    version_dir / "telemetry-agent-2.4.1-sources.jar",
    version_dir / "telemetry-agent-2.4.1.pom",
]:
    data = artifact.read_bytes()
    sha1 = hashlib.sha1(data).hexdigest() + "\n"
    md5 = hashlib.md5(data).hexdigest() + "\n"
    if (artifact.with_name(artifact.name + ".sha1")).read_text(encoding="ascii") != sha1:
        fail(f"{artifact.name}.sha1 does not match final artifact bytes or newline format")
    if (artifact.with_name(artifact.name + ".md5")).read_text(encoding="ascii") != md5:
        fail(f"{artifact.name}.md5 does not match final artifact bytes or newline format")

print("ok")
PY

status=$?
if [ "$status" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
  exit 0
else
  echo 0 > /logs/verifier/reward.txt
  exit "$status"
fi
