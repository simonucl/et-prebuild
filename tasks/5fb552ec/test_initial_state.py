# test_initial_state.py
#
# PyTest suite that validates the *initial* operating-system / filesystem state
# for the “collect ERROR logs” exercise **before** the student performs any
# actions.  It asserts that:
#   • The expected application log tree exists exactly as described.
#   • Every required *.log file is present and readable.
#   • ERROR–line counts inside each file match the specification.
#   • No extra *.log files are lurking under /home/user/app/logs.
#   • Nothing named /home/user/analysis* exists yet.
#
# Only the standard library + pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
APP_ROOT = HOME / "app"
LOG_DIR = APP_ROOT / "logs"
ANALYSIS_PREFIX = HOME / "analysis"

# --------------------------------------------------------------------------- #
# Expected log files and their respective ERROR-line counts
# --------------------------------------------------------------------------- #
EXPECTED_LOGS = {
    LOG_DIR / "auth.log": 2,
    LOG_DIR / "db.log": 0,
    LOG_DIR / "payment.log": 3,
    LOG_DIR / "old" / "archive.log": 1,
}


@pytest.fixture(scope="module")
def discovered_logs():
    """
    Walk the /home/user/app/logs tree and return a set of Path objects for all
    non-hidden *.log files discovered.  Hidden files/dirs (those whose basename
    starts with '.') are ignored.
    """
    found = set()
    for root, dirs, files in os.walk(LOG_DIR):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in files:
            if fname.startswith("."):
                continue  # ignore hidden files
            if fname.endswith(".log"):
                found.add(Path(root) / fname)
    return found


# --------------------------------------------------------------------------- #
# Tests for filesystem layout
# --------------------------------------------------------------------------- #
def test_log_directory_exists():
    assert LOG_DIR.is_dir(), f"Expected directory {LOG_DIR} to exist."


def test_expected_log_files_present_and_no_extras(discovered_logs):
    expected_set = set(EXPECTED_LOGS.keys())
    assert (
        discovered_logs == expected_set
    ), (
        "Mismatch in *.log files under /home/user/app/logs.\n"
        f"Expected exactly:\n  {sorted(str(p) for p in expected_set)}\n"
        f"Found:\n  {sorted(str(p) for p in discovered_logs)}"
    )


# --------------------------------------------------------------------------- #
# Tests for log contents
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("log_path, expected_error_count", EXPECTED_LOGS.items())
def test_log_error_line_counts(log_path, expected_error_count):
    assert log_path.is_file(), f"Missing log file: {log_path}"
    with log_path.open("r", encoding="utf-8") as fh:
        actual_count = sum("ERROR" in line for line in fh)
    assert (
        actual_count == expected_error_count
    ), (
        f"{log_path} should contain {expected_error_count} lines with 'ERROR' "
        f"but actually contains {actual_count}."
    )


# --------------------------------------------------------------------------- #
# Tests ensuring /home/user/analysis* does NOT pre-exist
# --------------------------------------------------------------------------- #
def test_analysis_directory_absent():
    # Any path that starts with '/home/user/analysis' must not exist yet.
    for path in HOME.iterdir():
        if path.name.startswith("analysis"):
            pytest.fail(
                f"Found pre-existing artefact '{path}'.\n"
                "The analysis directory and related files must NOT exist "
                "before the student runs their solution."
            )