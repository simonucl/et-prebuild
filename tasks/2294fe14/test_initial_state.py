# test_initial_state.py
"""
Pytest suite to validate the initial operating-system / filesystem state
BEFORE the student executes their solution script.

Checks performed:
1. The directory /home/user/performance exists.
2. The file /home/user/performance/running_containers.txt exists.
3. The file contains exactly four lines.
4. The lines match the expected container names in the correct order.

NOTE:
We intentionally do NOT check for the presence (or absence) of the
output file `/home/user/performance/running_containers_summary.log`
because the task instructions forbid testing any output artefacts.
"""

from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/performance")
INPUT_FILE = BASE_DIR / "running_containers.txt"

EXPECTED_LINES = [
    "redis",
    "nginx",
    "metrics_collector",
    "auth_service",
]


def test_performance_directory_exists():
    assert BASE_DIR.exists(), (
        f"The directory {BASE_DIR} is missing. "
        "It should exist before the student's command is run."
    )
    assert BASE_DIR.is_dir(), (
        f"{BASE_DIR} exists but is not a directory. "
        "It must be a directory."
    )


def test_running_containers_file_exists():
    assert INPUT_FILE.exists(), (
        f"The input file {INPUT_FILE} is missing. "
        "This file must be present so the student's command can count its lines."
    )
    assert INPUT_FILE.is_file(), (
        f"{INPUT_FILE} exists but is not a regular file."
    )


def test_running_containers_file_contents():
    contents = INPUT_FILE.read_text(encoding="utf-8")
    # Splitlines without keeping the newline characters.
    lines = contents.splitlines()
    assert len(lines) == 4, (
        f"{INPUT_FILE} should contain exactly 4 lines, "
        f"but {len(lines)} lines were found."
    )
    assert lines == EXPECTED_LINES, (
        f"The contents of {INPUT_FILE} do not match the expected lines.\n"
        f"Expected lines:\n{EXPECTED_LINES}\n"
        f"Actual lines:\n{lines}"
    )