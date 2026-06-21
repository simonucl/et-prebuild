# test_initial_state.py
#
# This test-suite verifies that the operating system / filesystem
# is in the expected *initial* state ­— i.e. **before** the student
# carries out any actions for the exercise “mobile build benchmark”.
#
# The required initial state is:
#   1. /home/user/mobile_build/dummy_build.sh must already exist,
#      be executable and contain the exact expected contents.
#   2. /home/user/mobile_build/logs may or may not exist yet,
#      but the benchmark log file MUST NOT exist.
#
# If any of these conditions are not met, the learner starts from
# an unexpected environment and subsequent grading will be invalid.

import os
import stat
import textwrap
import pytest
from pathlib import Path

HOME = Path("/home/user")
BUILD_DIR = HOME / "mobile_build"
DUMMY_SCRIPT = BUILD_DIR / "dummy_build.sh"
LOGS_DIR = BUILD_DIR / "logs"
BENCHMARK_LOG = LOGS_DIR / "benchmark_run1.log"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_executable(p: Path) -> bool:
    """Return True if *p* is marked as executable for the owner."""
    mode = p.stat().st_mode
    return bool(mode & stat.S_IXUSR)

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_dummy_build_script_exists_and_is_correct():
    """
    The pre-existing build script must be present, executable and
    match the expected hard-coded contents.
    """
    assert DUMMY_SCRIPT.exists(), (
        f"Required file {DUMMY_SCRIPT} is missing. "
        "The exercise assumes it is already present."
    )
    assert DUMMY_SCRIPT.is_file(), f"{DUMMY_SCRIPT} exists but is not a file."

    assert _is_executable(DUMMY_SCRIPT), (
        f"{DUMMY_SCRIPT} should have the executable bit set (mode 755)."
    )

    expected_contents = textwrap.dedent(
        """\
        #!/usr/bin/env bash
        # simple dummy build
        sleep 1
        echo "Dummy build finished"
        """
    ).strip()  # strip to ignore trailing newline differences

    with DUMMY_SCRIPT.open("r", encoding="utf-8") as fh:
        actual_contents = fh.read().strip()

    assert actual_contents == expected_contents, (
        f"{DUMMY_SCRIPT} contents differ from the expected template.\n"
        "If this file has been modified, the exercise cannot be graded "
        "reliably.\n"
        "Expected:\n"
        f"{expected_contents!r}\n"
        "Found:\n"
        f"{actual_contents!r}"
    )

def test_benchmark_log_not_present_yet():
    """
    Before the student performs the task, the benchmark log file must
    NOT already exist.  Its presence would indicate that the exercise
    has been inadvertently solved or the workspace is dirty.
    """
    assert not BENCHMARK_LOG.exists(), (
        f"{BENCHMARK_LOG} already exists. "
        "The initial state should not contain this file."
    )

@pytest.mark.parametrize("path", [LOGS_DIR])
def test_logs_directory_state(path: Path):
    """
    The logs directory itself may or may not exist initially
    (the instructions tell the student to create it *if not present*).
    This test asserts two acceptable states:
       • directory absent
       • directory present but not containing benchmark_run1.log yet
    """
    if not path.exists():
        pytest.skip(f"{path} does not exist yet – this is acceptable.")
    else:
        assert path.is_dir(), (
            f"{path} exists but is not a directory; "
            "it should either be a directory or absent."
        )
        # Ensure the benchmark log is not pre-existing (already checked),
        # but give a clearer failure if it is inside the existing dir.
        assert not BENCHMARK_LOG.exists(), (
            f"{BENCHMARK_LOG} found inside an existing logs directory. "
            "The benchmark must not be run before the exercise begins."
        )