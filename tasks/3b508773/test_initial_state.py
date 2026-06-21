# test_initial_state.py
#
# This test-suite validates the state of the operating system *before* the
# student runs their one-liner.  It asserts that:
#
# 1. /home/user/container_secrets.env exists and contains **exactly** the two
#    legacy credential lines, each terminated by a newline character.
# 2. /home/user/rotation.log is **absent**.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
SECRETS_FILE = HOME / "container_secrets.env"
ROTATION_LOG = HOME / "rotation.log"

LEGACY_LINES = [
    "DB_USER=legacy\n",
    "DB_PASS=OldP@ssword123\n",
]


def _read_file_lines(path: Path):
    """
    Helper that reads a text file in UTF-8 and returns a list
    of its lines **including** their trailing newline characters.
    Raises FileNotFoundError if the file is missing.
    """
    with path.open("r", encoding="utf-8") as f:
        return f.readlines()


def test_container_secrets_env_exists_and_is_correct():
    # 1. File must exist and be a regular file.
    assert SECRETS_FILE.exists(), (
        f"Expected {SECRETS_FILE} to exist, but it is missing."
    )
    assert SECRETS_FILE.is_file(), (
        f"Expected {SECRETS_FILE} to be a regular file."
    )

    # 2. Content must match the two legacy lines exactly.
    actual_lines = _read_file_lines(SECRETS_FILE)

    # Explanatory error messages for mismatches.
    assert actual_lines == LEGACY_LINES, (
        f"{SECRETS_FILE} content mismatch.\n"
        f"Expected exactly:\n{''.join(LEGACY_LINES)}\n"
        f"Found:\n{''.join(actual_lines)}"
    )

    # 3. Ensure there are precisely two lines.
    assert len(actual_lines) == 2, (
        f"{SECRETS_FILE} should contain exactly 2 lines, "
        f"but contains {len(actual_lines)}."
    )


def test_rotation_log_does_not_exist_yet():
    assert not ROTATION_LOG.exists(), (
        f"{ROTATION_LOG} should NOT exist before rotation, "
        f"but it is present."
    )