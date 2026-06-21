# test_initial_state.py
#
# Pytest suite that validates the filesystem *before* the student performs
# any actions.  It guarantees that the starting conditions for the task
# are exactly as described in the instructions.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

DATASET_DIR = Path("/home/user/datasets/coral_reef")
VERSION_FILE = DATASET_DIR / "VERSION"
CHANGELOG_FILE = DATASET_DIR / "CHANGELOG.md"
LOGS_DIR = DATASET_DIR / "logs"
LOG_FILE = LOGS_DIR / "version_bump.log"


def test_dataset_directory_exists_and_writable():
    assert DATASET_DIR.is_dir(), (
        f"Expected directory {DATASET_DIR} to exist, but it does not."
    )
    # Check write permission for the current user.
    assert os.access(DATASET_DIR, os.W_OK), (
        f"Directory {DATASET_DIR} exists but is not writable."
    )


def test_version_file_contains_1_2_3_newline_only():
    assert VERSION_FILE.is_file(), (
        f"Expected file {VERSION_FILE} to exist, but it does not."
    )

    raw = VERSION_FILE.read_bytes()
    expected = b"1.2.3\n"
    assert raw == expected, (
        f"{VERSION_FILE} should contain exactly {expected!r} "
        f"(length {len(expected)}), but contains {raw!r} "
        f"(length {len(raw)})."
    )


def test_changelog_initial_lines():
    """
    The first seven lines (including the blank line between versions)
    must match the specification exactly.
    """
    assert CHANGELOG_FILE.is_file(), (
        f"Expected file {CHANGELOG_FILE} to exist, but it does not."
    )

    expected_lines = [
        "## [1.2.3] - 2023-01-10\n",
        "### Added\n",
        "- Added January 2023 reef imagery.\n",
        "\n",
        "## [1.2.2] - 2022-12-20\n",
        "### Fixed\n",
        "- Corrected GPS coordinates.\n",
    ]

    with CHANGELOG_FILE.open("r", encoding="utf-8", newline="") as fh:
        actual_lines = [fh.readline() for _ in range(len(expected_lines))]

    assert actual_lines == expected_lines, (
        f"The first {len(expected_lines)} lines of {CHANGELOG_FILE} "
        "do not match the expected contents.\n"
        "Expected:\n"
        "".join(expected_lines)
        + "\nActual:\n"
        "".join(actual_lines)
    )


def test_logs_directory_absent():
    """
    The logs directory and the version_bump.log file must NOT exist
    before the student completes the task.
    """
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} should not exist yet, "
        "but it is present."
    )
    # If the directory is absent, the file must also be absent; we still test it for clarity.
    assert not LOG_FILE.exists(), (
        f"File {LOG_FILE} should not exist yet, but it is present."
    )