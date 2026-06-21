# test_initial_state.py
"""
Pytest suite that verifies the *initial* filesystem state for the
“inventory-builder” exercise, i.e. before the student runs any
solution code.

The tests assert that:
1. The provision directory exists.
2. The raw server list exists **and** contains the exact eight
   lines (duplicates & mixed-case included) described in the task.
3. No output artefacts created by the forthcoming student script
   are present yet (inventory.yml, convert.log).

Any deviation from this specification will fail with a clear,
actionable error message.
"""

import os
from pathlib import Path

import pytest

# Constants for paths used throughout the test suite
HOME = Path("/home/user")
PROVISION_DIR = HOME / "provision"
RAW_FILE = PROVISION_DIR / "servers_raw.txt"
OUTPUT_DIR = PROVISION_DIR / "output"
INVENTORY_YML = OUTPUT_DIR / "inventory.yml"
CONVERT_LOG = OUTPUT_DIR / "convert.log"

# The authoritative raw-file content (including the trailing newline)
EXPECTED_RAW_CONTENT = (
    "DB01\n"
    "web01\n"
    "app02\n"
    "web01\n"
    "app01\n"
    "db01\n"
    "WEB02\n"
    "app02\n"
)

EXPECTED_RAW_LINES = [
    "DB01",
    "web01",
    "app02",
    "web01",
    "app01",
    "db01",
    "WEB02",
    "app02",
]


def test_provision_directory_exists():
    """Ensure /home/user/provision/ is present and is a directory."""
    assert PROVISION_DIR.exists(), (
        f"Expected directory {PROVISION_DIR} is missing. "
        "The exercise requires this directory to be pre-created."
    )
    assert PROVISION_DIR.is_dir(), (
        f"{PROVISION_DIR} exists but is not a directory."
    )


def test_servers_raw_file_exists_and_has_correct_content():
    """Verify that servers_raw.txt exists and matches the exact expected lines."""
    assert RAW_FILE.exists(), (
        f"Required file {RAW_FILE} is missing."
    )
    assert RAW_FILE.is_file(), (
        f"{RAW_FILE} exists but is not a regular file."
    )

    # Read *binary* first to ensure byte-exact trailing newline,
    # then decode for easier line comparison / error messages.
    raw_bytes = RAW_FILE.read_bytes()
    raw_text = raw_bytes.decode("utf-8", "replace")

    # 1) Exact full-text match, including final newline
    assert raw_text == EXPECTED_RAW_CONTENT, (
        f"The contents of {RAW_FILE} do not match the expected initial data.\n"
        "---- Expected ----\n"
        f"{EXPECTED_RAW_CONTENT!r}\n"
        "---- Found ----\n"
        f"{raw_text!r}\n"
        "Ensure *no* edits have been made to the raw file."
    )

    # 2) Extra sanity: check split lines
    lines = raw_text.splitlines()
    assert lines == EXPECTED_RAW_LINES, (
        "Line-by-line comparison failed; the raw file must contain exactly the "
        "eight specified hostnames (case preserved, duplicates included) and "
        "nothing else."
    )


def test_no_output_files_yet():
    """
    Before the student runs any code, *no* output artefacts should be present.
    The tests tolerate the presence of the 'output' directory itself but
    will fail if either inventory.yml or convert.log already exist.
    """
    if OUTPUT_DIR.exists():
        assert OUTPUT_DIR.is_dir(), (
            f"{OUTPUT_DIR} exists but is not a directory."
        )
    else:
        # It's OK if the directory is entirely missing at this stage.
        pass

    assert not INVENTORY_YML.exists(), (
        f"{INVENTORY_YML} already exists, but it should be created by the "
        "student's solution script—not beforehand."
    )

    assert not CONVERT_LOG.exists(), (
        f"{CONVERT_LOG} already exists, but it should be created by the "
        "student's solution script—not beforehand."
    )