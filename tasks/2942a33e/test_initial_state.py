# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating system
# before the student’s solution is executed.  Nothing about the output file
# (/home/user/data/user_frequency.txt) is checked here, only the pre-existing
# log file that the student must read.

import collections
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

DATA_DIR = Path("/home/user/data")
LOG_FILE = DATA_DIR / "users.log"

EXPECTED_LOG_LINES = [
    "alice",
    "bob",
    "charlie",
    "alice",
    "bob",
    "alice",
    "dave",
    "eve",
    "bob",
    "charlie",
    "charlie",
    "charlie",
    "frank",
    "grace",
    "heidi",
    "ivan",
    "judy",
    "mallory",
    "oscar",
    "peggy",
    "trent",
    "victor",
    "walter",
    "peggy",
    "trent",
    "trent",
    "trent",
    "mallory",
    "mallory",
    "trent",
]

# Verified counts of each username in the initial log
EXPECTED_COUNTS = {
    "alice": 3,
    "bob": 3,
    "charlie": 4,
    "dave": 1,
    "eve": 1,
    "frank": 1,
    "grace": 1,
    "heidi": 1,
    "ivan": 1,
    "judy": 1,
    "mallory": 3,
    "oscar": 1,
    "peggy": 2,
    "trent": 5,
    "victor": 1,
    "walter": 1,
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_log_file():
    """
    Returns the raw text and the list of lines (without trailing newlines) from
    /home/user/data/users.log.  A single trailing newline at EOF is mandatory.
    """
    raw_text = LOG_FILE.read_text(encoding="utf-8")
    lines = raw_text.rstrip("\n").split("\n") if raw_text else []
    return raw_text, lines


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_data_directory_exists():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


def test_log_file_exists_and_is_file():
    assert LOG_FILE.exists(), f"Required log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_log_file_content_exact_match():
    raw_text, lines = read_log_file()

    # 1. File must end with exactly one newline character
    assert raw_text.endswith("\n"), (
        f"{LOG_FILE} must end with a single newline character."
    )
    assert not raw_text.endswith("\n\n"), (
        f"{LOG_FILE} appears to contain more than one trailing newline."
    )

    # 2. No leading/trailing blank lines
    assert lines[0], f"{LOG_FILE} starts with a blank line."
    assert lines[-1], f"{LOG_FILE} ends with a blank line before the final newline."

    # 3. Exact line-by-line match with expected sequence
    assert lines == EXPECTED_LOG_LINES, (
        f"{LOG_FILE} contents do not match the expected initial lines.\n"
        f"Expected:\n{EXPECTED_LOG_LINES}\n\nFound:\n{lines}"
    )


def test_log_file_username_counts():
    """
    Verify that the multiplicity of each username inside users.log matches the
    specification.  This is a stronger check than simply comparing the list,
    and will raise a clearer error message if counts are wrong.
    """
    _, lines = read_log_file()
    counter = collections.Counter(lines)

    # Check for missing or incorrect counts
    for user, expected_count in EXPECTED_COUNTS.items():
        actual_count = counter.get(user, 0)
        assert actual_count == expected_count, (
            f"Username '{user}' should occur {expected_count} times in "
            f"{LOG_FILE}, but {actual_count} occurrence(s) were found."
        )

    # Check for any unexpected usernames
    unexpected_users = set(counter) - set(EXPECTED_COUNTS)
    assert not unexpected_users, (
        f"{LOG_FILE} contains unexpected username(s): {sorted(unexpected_users)}"
    )