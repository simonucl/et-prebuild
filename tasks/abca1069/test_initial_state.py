# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state for the “repeatable micro-benchmark harness” exercise.
#
# These checks **must** run before the student takes any action, therefore the
# artefacts that the assignment asks the student to create (directory,
# script, CSV, log) must **not** exist yet.
#
# If any of those artefacts already exist, something is wrong with the clean
#-room environment and the test should fail with a clear, actionable message.
#
# Only the presence of system-supplied prerequisites (e.g. /usr/bin/time) is
# validated positively.

import os
import stat
from pathlib import Path

BENCH_DIR = Path("/home/user/benchmarks")
SCRIPT_PATH = BENCH_DIR / "run_benchmarks.sh"
CSV_PATH = BENCH_DIR / "benchmark_summary.csv"
LOG_PATH = BENCH_DIR / "raw_benchmark.log"
TIME_CMD = Path("/usr/bin/time")


def _human(path: Path) -> str:
    """Return a human-readable string for a path (avoids double slashes)."""
    return str(path.resolve())


def test_system_has_time_command():
    """The host system must provide /usr/bin/time and it must be executable."""
    assert TIME_CMD.exists(), (
        f"Required tool {_human(TIME_CMD)} is missing. "
        "The assignment cannot be completed without GNU 'time'."
    )
    # Executable bit for the current user
    is_executable = os.access(TIME_CMD, os.X_OK)
    assert is_executable, (
        f"Required tool {_human(TIME_CMD)} exists but is not executable."
    )


def test_benchmark_directory_absent():
    """
    The workspace directory must NOT exist before the student runs their
    provisioning code.  This guarantees a clean start and avoids stale data.
    """
    assert not BENCH_DIR.exists(), (
        f"Found unexpected directory {_human(BENCH_DIR)}. "
        "The grading environment should start without this directory; "
        "make sure you are running the tests on a pristine workspace."
    )


def test_script_does_not_exist_yet():
    """The benchmark runner script must not be present at the outset."""
    assert not SCRIPT_PATH.exists(), (
        f"Found unexpected script {_human(SCRIPT_PATH)}. "
        "The student has not created it yet, so it must be absent."
    )


def test_output_files_do_not_exist_yet():
    """Neither the CSV summary nor the raw log file should exist initially."""
    for path in (CSV_PATH, LOG_PATH):
        assert not path.exists(), (
            f"Found unexpected file {_human(path)}. "
            "No benchmark data should exist before the student runs the script."
        )