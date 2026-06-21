# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student performs any certificate-migration steps.
#
# DO NOT modify this file.  If any of these tests fail, the starting
# environment is not what the task description promises and the
# student should not begin the migration procedure.

import os
from pathlib import Path

HOME = Path("/home/user")
MICROSERVICES_DIR = HOME / "microservices"
GATEWAY_DIR = MICROSERVICES_DIR / "gateway"
CERTS_DIR = MICROSERVICES_DIR / "certs"
CONFIG_PATH = GATEWAY_DIR / "config.yaml"
OLD_CERT_PATH = CERTS_DIR / "old_cert.pem"
OLD_KEY_PATH = CERTS_DIR / "old_key.pem"
NEW_CERT_PATH = CERTS_DIR / "new_cert.pem"
NEW_KEY_PATH = CERTS_DIR / "new_key.pem"
MIGRATION_LOGS_DIR = HOME / "migration_logs"


def test_required_directories_exist():
    """
    The three canonical directories must exist before any action is taken.
    """
    for path in (MICROSERVICES_DIR, GATEWAY_DIR, CERTS_DIR):
        assert path.is_dir(), f"Expected directory {path} to exist in the initial state."


def test_placeholder_cert_and_key_exist():
    """
    The old, soon-to-expire certificate/key pair must be present before migration.
    """
    for path in (OLD_CERT_PATH, OLD_KEY_PATH):
        assert path.is_file(), f"Missing placeholder file expected in initial state: {path}"


def test_new_cert_and_key_do_not_exist_yet():
    """
    The new certificate/key should *not* exist before migration begins.
    """
    for path in (NEW_CERT_PATH, NEW_KEY_PATH):
        assert not path.exists(), (
            f"{path} should NOT exist yet. "
            "The student must generate it as part of the task."
        )


def test_migration_logs_directory_absent():
    """
    /home/user/migration_logs/ must not pre-exist.  The student will create it.
    """
    assert not MIGRATION_LOGS_DIR.exists(), (
        f"Directory {MIGRATION_LOGS_DIR} should NOT exist before migration starts."
    )


def test_gateway_config_yaml_contents():
    """
    config.yaml must exactly match the three-line block (four lines incl. 'ssl:' row)
    specified in the task description, *and* it must still reference the OLD cert/key.
    """
    expected_content = (
        "ssl:\n"
        "  cert: ../certs/old_cert.pem\n"
        "  key : ../certs/old_key.pem\n"
        "mode: production\n"
    )

    assert CONFIG_PATH.is_file(), f"Expected gateway config file missing: {CONFIG_PATH}"

    actual = CONFIG_PATH.read_text()

    # 1. Exact content check (including newline terminator)
    assert actual == expected_content, (
        f"{CONFIG_PATH} contents differ from the expected initial state.\n"
        "---- Expected ----\n"
        f"{expected_content}"
        "----   Found  ----\n"
        f"{actual}"
        "------------------"
    )

    # 2. Defensive sanity: ensure it does *not* already point to new_cert/new_key
    assert "new_cert.pem" not in actual, "config.yaml already references new_cert.pem; it should not."
    assert "new_key.pem" not in actual, "config.yaml already references new_key.pem; it should not."