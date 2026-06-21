# test_initial_state.py
#
# This pytest suite verifies that the initial filesystem state is correct
# *before* the student performs any actions.  It checks only the artefacts
# that are supposed to exist at the very start of the exercise.
#
# Rules respected:
#   • Uses only stdlib + pytest
#   • Does NOT touch or test for any output files/directories
#   • Provides clear failure messages when something is missing or malformed

import os
import stat
import pytest

BUILD_DIR = "/home/user/build"
INVENTORY_CSV = os.path.join(BUILD_DIR, "inventory.csv")

# The exact, byte-for-byte content the inventory.csv file must have,
# including the trailing newline after the last line.
EXPECTED_INVENTORY_CONTENT = (
    "artifact,version,sha256\n"
    "core-lib,1.2.3,abc123def456\n"
    "ui-module,2.0.0-rc1,789abc012def\n"
    "cli-tool,0.9.8,fedcba987654\n"
)


def test_build_directory_exists():
    """Ensure /home/user/build directory is present and is a directory."""
    assert os.path.exists(BUILD_DIR), (
        f"Required directory {BUILD_DIR} does not exist."
    )
    assert os.path.isdir(BUILD_DIR), (
        f"{BUILD_DIR} exists but is not a directory."
    )


def test_inventory_csv_exists():
    """Ensure inventory.csv exists inside the build directory."""
    assert os.path.exists(INVENTORY_CSV), (
        f"Required file {INVENTORY_CSV} is missing."
    )
    assert os.path.isfile(INVENTORY_CSV), (
        f"{INVENTORY_CSV} exists but is not a regular file."
    )


def test_inventory_csv_mode_readable():
    """inventory.csv should be readable by the current user."""
    st_mode = os.stat(INVENTORY_CSV).st_mode
    is_readable = bool(st_mode & stat.S_IRUSR)
    assert is_readable, (
        f"{INVENTORY_CSV} is not readable by the current user."
    )


def test_inventory_csv_content_exact():
    """
    Validate that inventory.csv contains exactly the expected data
    (including the final newline) and nothing else.
    """
    with open(INVENTORY_CSV, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Exact match
    assert content == EXPECTED_INVENTORY_CONTENT, (
        "The contents of inventory.csv do not match the expected template.\n"
        "Expected:\n"
        f"{EXPECTED_INVENTORY_CONTENT!r}\n"
        "Found:\n"
        f"{content!r}"
    )

    # 2. Ensure file ends with a single newline (implicit in equality check),
    #    but give a clearer error message for common pitfalls.
    assert content.endswith("\n"), (
        "inventory.csv must end with a single Unix LF newline."
    )

    # 3. Ensure there is no extra blank line at the end (already covered by
    #    the exact equality check, but keep a focused assertion for clarity).
    assert not content.endswith("\n\n"), (
        "inventory.csv has an extra blank line at the end."
    )