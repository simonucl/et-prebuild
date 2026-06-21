# test_initial_state.py
#
# Pytest suite to validate the machine’s initial state *before*
# the student executes any commands for the “transform hosts file”
# exercise.  These tests assert that all prerequisites are in place
# and that no artefacts from a previous run already exist.

import os
from pathlib import Path

DEPLOY_DIR = Path("/home/user/deploy")
TARGETS_TXT = DEPLOY_DIR / "targets.txt"
TARGETS_ARRAY_SH = DEPLOY_DIR / "targets_array.sh"
TRANSFORM_LOG = DEPLOY_DIR / "transform.log"

EXPECTED_TARGETS_CONTENT = (
    "web-01\n"
    "web-02\n"
    "api-01\n"
    "db-01\n"
)  # exactly four lines plus final newline


def test_deploy_directory_exists_and_writable():
    assert DEPLOY_DIR.exists(), f"Required directory {DEPLOY_DIR} is missing."
    assert DEPLOY_DIR.is_dir(), f"{DEPLOY_DIR} exists but is not a directory."
    # Confirm we can create files (write permission for current user)
    assert os.access(DEPLOY_DIR, os.W_OK), (
        f"Directory {DEPLOY_DIR} is not writable by the current user."
    )


def test_targets_txt_exists_and_has_expected_content():
    assert TARGETS_TXT.exists(), f"Source file {TARGETS_TXT} is missing."
    assert TARGETS_TXT.is_file(), f"{TARGETS_TXT} exists but is not a regular file."

    content = TARGETS_TXT.read_text(encoding="utf-8")
    assert content == EXPECTED_TARGETS_CONTENT, (
        f"{TARGETS_TXT} does not contain the expected host list.\n"
        "Expected exact byte string (␊ denotes newline):\n"
        "web-01␊web-02␊api-01␊db-01␊\n"
        f"Actual content was:\n{repr(content)}"
    )


def test_output_files_do_not_exist_yet():
    assert not TARGETS_ARRAY_SH.exists(), (
        f"Output file {TARGETS_ARRAY_SH} already exists—initial state should be clean."
    )
    assert not TRANSFORM_LOG.exists(), (
        f"Log file {TRANSFORM_LOG} already exists—initial state should be clean."
    )