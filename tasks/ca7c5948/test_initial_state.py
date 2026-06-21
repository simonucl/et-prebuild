# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student performs any action.
#
# Rules respected:
#   • Only uses Python stdlib + pytest.
#   • Tests rely on absolute paths.
#   • Does NOT inspect or mention any output files/directories that the
#     student is expected to create later (/home/user/datasets/reports/*).

from pathlib import Path
import re
import pytest

# Absolute path to the pre-existing log file
LOG_PATH = Path("/home/user/datasets/logs/cleaning.log")

# Regular-expression patterns that must appear in the log and capture integers
PATTERNS = {
    "loaded":        re.compile(r"Loaded\s+(?P<val>\d+)\s+rows", re.IGNORECASE),
    "missing":       re.compile(r"Removed\s+(?P<val>\d+)\s+rows?\s+with\s+missing\s+values", re.IGNORECASE),
    "out_of_range":  re.compile(r"Removed\s+(?P<val>\d+)\s+rows?\s+with\s+out[-_]of[-_]range\s+values", re.IGNORECASE),
    "duplicate":     re.compile(r"Removed\s+(?P<val>\d+)\s+duplicate\s+rows?", re.IGNORECASE),
    "remaining":     re.compile(r"Finished\s+cleaning\s+successfully:\s+(?P<val>\d+)\s+rows?\s+remaining", re.IGNORECASE),
}


@pytest.fixture(scope="module")
def log_text():
    """
    Loads the entire text of /home/user/datasets/logs/cleaning.log
    and fails early with a clear message if the file is missing.
    """
    assert LOG_PATH.is_file(), (
        f"Expected log file not found at {LOG_PATH}. "
        "Ensure the automatic cleaning script generated this file."
    )
    return LOG_PATH.read_text(encoding="utf-8", errors="replace")


def _extract_value(pattern: re.Pattern, text: str, key: str) -> int:
    """
    Helper that extracts an integer value from text using 'pattern'.
    Raises an AssertionError with a clear message if the pattern is missing.
    """
    match = pattern.search(text)
    assert match, (
        f"Unable to find the '{key}' value in {LOG_PATH}. "
        f"Expected a line matching /{pattern.pattern}/."
    )
    return int(match.group("val"))


def test_log_contains_required_counts(log_text):
    """
    Verifies that the log contains all required numeric counts and that the
    counts are internally consistent.
    """
    # Extract all numeric values
    counts = {
        key: _extract_value(pattern, log_text, key)
        for key, pattern in PATTERNS.items()
    }

    loaded       = counts["loaded"]
    missing      = counts["missing"]
    out_of_range = counts["out_of_range"]
    duplicate    = counts["duplicate"]
    remaining    = counts["remaining"]

    removed_total = missing + out_of_range + duplicate

    # Internal consistency checks with explicit failure messages
    assert removed_total == loaded - remaining, (
        "Row-count mismatch:\n"
        f"  LOADED         = {loaded}\n"
        f"  REMAINING      = {remaining}\n"
        f"  Derived REMOVED_TOTAL (MISSING+OUT_OF_RANGE+DUPLICATE) = {removed_total}\n"
        "Expected: LOADED - REMAINING == REMOVED_TOTAL."
    )

    # Spot-check the exact expected integers so the student gets immediate feedback
    # if the initial fixture data ever changes.
    assert loaded == 4789,     f"Expected LOADED=4789, found {loaded}"
    assert remaining == 4598,  f"Expected REMAINING=4598, found {remaining}"
    assert missing == 123,     f"Expected MISSING=123, found {missing}"
    assert out_of_range == 56, f"Expected OUT_OF_RANGE=56, found {out_of_range}"
    assert duplicate == 12,    f"Expected DUPLICATE=12, found {duplicate}"