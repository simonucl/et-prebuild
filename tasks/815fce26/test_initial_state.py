# test_initial_state.py
#
# Pytest suite that verifies the operating-system state **before**
# the student starts working on the task.
#
# It checks only the pre-existing input artefacts and never refers
# to any file that the student is supposed to create later.

import os
import re
from pathlib import Path

ENV_SETUP_DIR = Path("/home/user/env_setup")
TARGETS_TXT = ENV_SETUP_DIR / "targets.txt"

# The exact, canonical contents that must already be present
EXPECTED_LINES = [
    "dev",
    "qa",
    "staging",
    "qa",
    "dev",
    "prod",
    "qa",
]


def test_env_setup_directory_exists():
    """The /home/user/env_setup directory must exist and be a directory."""
    assert ENV_SETUP_DIR.exists(), (
        f"Required directory {ENV_SETUP_DIR} is missing."
    )
    assert ENV_SETUP_DIR.is_dir(), (
        f"{ENV_SETUP_DIR} exists but is not a directory."
    )


def test_targets_txt_exists_and_is_file():
    """targets.txt must exist and be a regular file."""
    assert TARGETS_TXT.exists(), (
        f"Required file {TARGETS_TXT} is missing."
    )
    assert TARGETS_TXT.is_file(), (
        f"{TARGETS_TXT} exists but is not a regular file."
    )


def test_targets_txt_content_and_format():
    """
    Validate that:
    1. Every line contains only lowercase letters (a-z).
    2. There are no empty lines.
    3. The overall content matches the expected canonical list.
    4. The file ends with a single trailing newline.
    """
    raw_bytes = TARGETS_TXT.read_bytes()
    # Ensure the file ends with exactly one trailing newline
    assert raw_bytes.endswith(b"\n"), (
        f"{TARGETS_TXT} must end with exactly one trailing newline."
    )

    # Decode and split into lines without removing empty ones
    # so we can detect stray blank lines.
    text = raw_bytes.decode("utf-8")
    lines = text.split("\n")[:-1]  # drop the last empty item after trailing '\n'

    # Check for empty lines _within_ the file (there should be none).
    assert all(line != "" for line in lines), (
        f"{TARGETS_TXT} contains empty lines; expected none."
    )

    # Regex validation: only lowercase letters a-z allowed.
    invalid = [line for line in lines if not re.fullmatch(r"[a-z]+", line)]
    assert not invalid, (
        f"{TARGETS_TXT} has invalid lines (only lowercase letters allowed): "
        f"{', '.join(invalid)}"
    )

    # Content must exactly match the canonical list (order matters).
    assert lines == EXPECTED_LINES, (
        f"{TARGETS_TXT} content mismatch.\n"
        f"Expected:\n{EXPECTED_LINES}\n\nFound:\n{lines}"
    )