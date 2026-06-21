# test_initial_state.py
#
# Pytest suite that verifies the workstation’s initial state
# BEFORE the student starts working.  Failures will tell the
# learner exactly what prerequisite is missing or incorrect.
#
# Rules:
#   • Uses only stdlib + pytest.
#   • Does NOT look for any output artefacts the student
#     is supposed to create later.
#   • All paths are absolute and case-sensitive.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
LOG_DIR = HOME / "docs" / "logs"

# ---------------------------------------------------------------------------
# Helper – canonical expectations for each *.log file (including the final LF)
# ---------------------------------------------------------------------------

EXPECTED_CONTENTS = {
    "app1.log": (
        "INFO Starting application\n"
        "WARNING Disk space almost full\n"
        "ERROR Failed to open configuration\n"
        "INFO Retrying startup\n"
        "ERROR Aborted\n"
    ),
    "app2.log": (
        "INFO Initialising\n"
        "INFO Running main loop\n"
        "INFO Shutdown complete\n"
    ),
    "app3.log": (
        "ERROR Crash detected\n"
        "WARNING Possible memory leak\n"
        "ERROR Stack trace follows\n"
        "WARNING Memory leak suspected\n"
        "INFO Attempting restart\n"
        "INFO Restart successful\n"
    ),
}

# --------------------------
# Tests for the initial state
# --------------------------

def test_logs_directory_exists():
    """The logs directory must exist and be a directory."""
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_exact_log_files_present():
    """
    The logs directory must contain exactly the expected *.log files
    (non-recursive) and nothing more.
    """
    expected_files = set(EXPECTED_CONTENTS.keys())
    found_files = {p.name for p in LOG_DIR.iterdir() if p.is_file() and p.suffix == ".log"}
    missing = expected_files - found_files
    extra = found_files - expected_files
    assert not missing, f"Missing log files in {LOG_DIR}: {', '.join(sorted(missing))}"
    assert not extra, f"Unexpected extra *.log files in {LOG_DIR}: {', '.join(sorted(extra))}"


@pytest.mark.parametrize("filename, expected_text", EXPECTED_CONTENTS.items())
def test_log_file_contents(filename, expected_text):
    """
    Each *.log file must contain the exact, case-sensitive lines specified in
    the task description (including the trailing newline).
    """
    file_path = LOG_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} does not exist."
    content = file_path.read_text(encoding="utf-8")
    assert content == expected_text, (
        f"Contents of {file_path} do not match the expected initial state.\n\n"
        f"--- Expected ({len(expected_text)} bytes) ---\n{expected_text}"
        f"--- Found ({len(content)} bytes) ---\n{content}"
    )