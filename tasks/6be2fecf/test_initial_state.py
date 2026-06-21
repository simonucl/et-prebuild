# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student performs any actions for the “sample-app” support-bundle
# exercise.  These tests purposely *fail* if the end-state artifacts
# (support_bundle directory or support_bundle.tar.gz) already exist,
# since they must be created by the student later.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SAMPLE_APP_DIR = HOME / "sample-app"
SUPPORT_BUNDLE_DIR = HOME / "support_bundle"
SUPPORT_BUNDLE_TAR = HOME / "support_bundle.tar.gz"


# ---------------------------
# Helpers / expected contents
# ---------------------------

EXPECTED_CONFIG_YAML = (
    b"app:\n"
    b"  name: Sample App\n"
    b"  version: \"1.2.3\"\n"
    b"server:\n"
    b"  port: 8080\n"
    b"logging:\n"
    b"  level: INFO\n"
)

EXPECTED_ENV_VARS = (
    b"PATH=/usr/local/bin:/usr/bin:/bin\n"
    b"JAVA_HOME=/usr/lib/jvm/default-java\n"
    b"SAMPLE_APP_OPTS=-Xmx256m\n"
)

EXPECTED_APP_LOG = (
    b"2023-10-02 10:40:01 INFO Starting Sample App version 1.2.3\n"
    b"2023-10-02 10:40:05 INFO Listening on port 8080\n"
    b"2023-10-02 10:41:33 WARN Cache miss for key user:42\n"
    b"2023-10-02 10:42:07 ERROR Failed to connect to database\n"
)

EXPECTED_STATUS_TXT = (
    b"\xe2\x97\x8f sample-app.service - Sample App Service\n"
    b"   Loaded: loaded (/etc/systemd/system/sample-app.service; enabled; vendor preset: enabled)\n"
    b"   Active: active (running) since Mon 2023-10-02 10:40:00 UTC; 2h 05min ago\n"
    b" Main PID: 1234 (java)\n"
    b"    Tasks: 14 (limit: 4915)\n"
    b"   Memory: 150.7M\n"
    b"   CGroup: /system.slice/sample-app.service\n"
    b"           \xe2\x94\x9c\xe2\x94\x80 1234 /usr/bin/java -jar /opt/sample-app.jar\n"
)

# ---------------------------
# Tests
# ---------------------------

def test_sample_app_directory_exists():
    """Verify /home/user/sample-app directory structure is present."""
    assert SAMPLE_APP_DIR.is_dir(), (
        "Expected directory '/home/user/sample-app' is missing."
    )

    logs_dir = SAMPLE_APP_DIR / "logs"
    assert logs_dir.is_dir(), (
        "Expected sub-directory '/home/user/sample-app/logs' is missing."
    )


@pytest.mark.parametrize(
    "path, expected_bytes, description",
    [
        (SAMPLE_APP_DIR / "config.yaml", EXPECTED_CONFIG_YAML, "config.yaml"),
        (SAMPLE_APP_DIR / "env_vars", EXPECTED_ENV_VARS, "env_vars"),
        (SAMPLE_APP_DIR / "logs" / "app.log", EXPECTED_APP_LOG, "app.log"),
        (SAMPLE_APP_DIR / "status.txt", EXPECTED_STATUS_TXT, "status.txt"),
    ],
)
def test_required_files_exist_and_match(path: Path, expected_bytes: bytes, description: str):
    """Each required file exists and is byte-for-byte identical to the canonical content."""
    assert path.is_file(), f"Required file '{path}' ({description}) is missing."

    actual = path.read_bytes()
    assert actual == expected_bytes, (
        f"Contents of '{path}' ({description}) do NOT match the expected initial state.\n"
        "Do not modify the source artefacts."
    )


def test_support_bundle_not_yet_present():
    """
    The support bundle directory and tarball should NOT exist yet.
    The student will create them during the exercise.
    """
    assert not SUPPORT_BUNDLE_DIR.exists(), (
        "Directory '/home/user/support_bundle' exists *before* the exercise starts.\n"
        "It should be created by the student; remove it to reset the environment."
    )
    assert not SUPPORT_BUNDLE_TAR.exists(), (
        "Archive '/home/user/support_bundle.tar.gz' exists *before* the exercise starts.\n"
        "It should be created by the student; remove it to reset the environment."
    )