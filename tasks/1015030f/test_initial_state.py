# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating system /
# filesystem before the student executes any commands for the deployment task.
#
# It confirms that:
#   1. /home/user/release exists and is writable.
#   2. /home/user/release/.env exists and contains the exact three-line block:
#        APP_NAME=webapp
#        APP_ENV=production
#        APP_VERSION=1.4.2
#      …with NO trailing blank lines or trailing newline character.
#   3. No “logs” directory (or deployment.log file) exists yet inside
#      /home/user/release.
#
# If any of these assertions fail, the accompanying message pinpoints exactly
# what is missing or incorrect.

import os
from pathlib import Path

RELEASE_DIR = Path("/home/user/release")
ENV_FILE = RELEASE_DIR / ".env"
LOGS_DIR = RELEASE_DIR / "logs"
DEPLOY_LOG = LOGS_DIR / "deployment.log"


def test_release_directory_exists_and_writable():
    assert RELEASE_DIR.exists(), (
        f"Expected directory {RELEASE_DIR} to exist, but it is missing."
    )
    assert RELEASE_DIR.is_dir(), (
        f"Expected {RELEASE_DIR} to be a directory, but it is not."
    )
    assert os.access(RELEASE_DIR, os.W_OK), (
        f"Directory {RELEASE_DIR} is not writable by the current user."
    )


def test_env_file_contents_are_pristine():
    assert ENV_FILE.exists(), (
        f"Expected file {ENV_FILE} to exist, but it is missing."
    )
    assert ENV_FILE.is_file(), (
        f"Expected {ENV_FILE} to be a regular file."
    )

    raw = ENV_FILE.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError(f"{ENV_FILE} is not valid UTF-8: {exc}") from exc

    # Ensure there is NO trailing newline character
    assert not text.endswith("\n"), (
        f"{ENV_FILE} must not end with a newline character."
    )

    lines = text.split("\n")
    assert len(lines) == 3, (
        f"{ENV_FILE} must contain exactly 3 lines, found {len(lines)}."
    )

    expected_lines = [
        "APP_NAME=webapp",
        "APP_ENV=production",
        "APP_VERSION=1.4.2",
    ]
    assert lines == expected_lines, (
        f"{ENV_FILE} contents mismatch.\n"
        f"Expected:\n{expected_lines}\nGot:\n{lines}"
    )


def test_logs_directory_absent():
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} should NOT exist yet."
    )
    # If someone accidentally created the file instead of a directory.
    assert not DEPLOY_LOG.exists(), (
        f"File {DEPLOY_LOG} should NOT exist yet."
    )