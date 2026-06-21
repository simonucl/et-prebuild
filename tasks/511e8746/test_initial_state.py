# test_initial_state.py
#
# This pytest suite verifies that the *starting* filesystem state is correct
# before the student attempts the exercise “Generate an aggregated error–code
# frequency report using sort + uniq”.
#
# It checks ONLY the _pre-existing_ artefacts that are required for the task:
#   • The directory /home/user/logs/ must exist.
#   • The files /home/user/logs/app1.log and /home/user/logs/app2.log must exist,
#     be readable regular files, and contain the exact log data that the task
#     description promises (so that later frequency calculations start from a
#     known truth).
#
# Per instructions we deliberately do *not* test for the presence (or absence)
# of the eventual output file error_frequency.csv — that belongs to the
# post-task validation, not the initial-state check.
#
# The assertions include clear, actionable failure messages so that missing or
# incorrect setup can be diagnosed quickly.

import re
from pathlib import Path

import pytest

LOG_DIR = Path("/home/user/logs")
APP1 = LOG_DIR / "app1.log"
APP2 = LOG_DIR / "app2.log"

# Expected per-file error-code frequencies (derived from the HTML truth value)
EXPECTED_FREQUENCIES = {
    APP1: {"E102": 3, "E104": 1, "E108": 1},
    APP2: {"E102": 3, "E104": 3, "E108": 2, "E114": 2},
}


def extract_error_codes(text: str):
    """
    Return a list of error-codes (E###) found in *text* in the same order as they
    appear.  The regex strictly enforces an uppercase 'E' followed by exactly
    three digits, as specified in the task description.
    """
    return re.findall(r"E[0-9]{3}", text)


@pytest.mark.parametrize("path", [LOG_DIR])
def test_log_directory_present(path):
    assert path.exists(), f"Directory {path} is missing — the logs folder must exist."
    assert path.is_dir(), f"Path {path} exists but is not a directory."


@pytest.mark.parametrize("log_path", [APP1, APP2])
def test_log_files_present_and_readable(log_path):
    assert log_path.exists(), f"Required log file {log_path} is missing."
    assert log_path.is_file(), f"{log_path} exists but is not a regular file."
    # Attempt to open to ensure readability
    try:
        content = log_path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {log_path}: {exc}")
    assert content.strip(), f"{log_path} is empty — it must contain log lines."


@pytest.mark.parametrize("log_path,expected_counts", EXPECTED_FREQUENCIES.items())
def test_log_file_contents_match_truth(log_path: Path, expected_counts: dict):
    """
    Confirm that each log file contains exactly the expected error-codes with the
    expected frequencies.  This guards against silent test failures later on
    due to a tampered or incomplete dataset.
    """
    content = log_path.read_text(encoding="utf-8")
    codes = extract_error_codes(content)

    # Compute actual frequencies
    actual_counts = {}
    for code in codes:
        actual_counts[code] = actual_counts.get(code, 0) + 1

    # Check that no unexpected codes slipped in
    unexpected = set(actual_counts) - set(expected_counts)
    assert not unexpected, (
        f"{log_path} contains unexpected error-codes: {sorted(unexpected)} "
        f"(expected only {sorted(expected_counts)})"
    )

    # Check that all expected codes are present with correct counts
    for code, expected_count in expected_counts.items():
        actual = actual_counts.get(code, 0)
        assert actual == expected_count, (
            f"In {log_path} the code {code} should appear {expected_count} times, "
            f"but found {actual} occurrence(s)."
        )