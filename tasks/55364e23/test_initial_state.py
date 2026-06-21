# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state before the student runs any commands for the “workflow timing”
# task.

import os
import stat
from pathlib import Path

# --- Paths that must already exist ------------------------------------------
SCRIPTS_DIR          = Path("/home/user/scripts")
WORKFLOW_SCRIPT      = SCRIPTS_DIR / "workflow.sh"
GNU_TIME_BINARY      = Path("/usr/bin/time")

# --- Paths that must *not* exist yet ----------------------------------------
PERF_REPORTS_DIR     = Path("/home/user/perf_reports")
PERF_REPORTS_LOGFILE = PERF_REPORTS_DIR / "workflow_time.log"


def _is_executable(file_path: Path) -> bool:
    """
    Return True if the current process can execute `file_path`.
    """
    return (
        file_path.is_file() and
        os.access(file_path, os.X_OK) and
        (file_path.stat().st_mode & stat.S_IXUSR)
    )


# --------------------------------------------------------------------------- #
# Positive pre-conditions: things that MUST already be present
# --------------------------------------------------------------------------- #
def test_scripts_directory_exists():
    assert SCRIPTS_DIR.exists(), (
        f"Expected directory {SCRIPTS_DIR} to exist, but it is missing."
    )
    assert SCRIPTS_DIR.is_dir(), (
        f"Expected {SCRIPTS_DIR} to be a directory, but it is not."
    )


def test_workflow_script_exists_and_executable():
    assert WORKFLOW_SCRIPT.exists(), (
        f"Expected script {WORKFLOW_SCRIPT} to exist, but it is missing."
    )
    assert WORKFLOW_SCRIPT.is_file(), (
        f"Expected {WORKFLOW_SCRIPT} to be a regular file."
    )
    assert _is_executable(WORKFLOW_SCRIPT), (
        f"Script {WORKFLOW_SCRIPT} is not marked executable."
    )


def test_workflow_script_contents_intact():
    """
    Optional but useful sanity check: ensure the student has not modified the
    baseline script in a way that would affect timing numbers.
    """
    expected_lines = [
        "#!/usr/bin/env bash",
        "# Simulated workflow",
        "sleep 0.05",
        'echo "Workflow step completed"',
    ]
    with WORKFLOW_SCRIPT.open("r", encoding="utf-8") as f:
        contents = f.read().strip().splitlines()

    for expected in expected_lines:
        assert any(expected in line for line in contents), (
            f"Did not find expected text {expected!r} inside {WORKFLOW_SCRIPT}."
        )


def test_gnu_time_binary_available():
    assert GNU_TIME_BINARY.exists(), (
        "GNU time binary (/usr/bin/time) is required for this task but was "
        "not found."
    )
    assert _is_executable(GNU_TIME_BINARY), (
        "/usr/bin/time exists but is not executable."
    )


# --------------------------------------------------------------------------- #
# Negative pre-conditions: things that MUST NOT exist prior to the action
# --------------------------------------------------------------------------- #
def test_perf_reports_directory_absent_initially():
    """
    The /home/user/perf_reports directory should not exist *before* the
    student runs their command.  Its creation is part of the assignment.
    """
    assert not PERF_REPORTS_DIR.exists(), (
        f"Directory {PERF_REPORTS_DIR} already exists, but it should be "
        "created by the student's command."
    )


def test_perf_reports_logfile_absent_initially():
    """
    Likewise, the final log file should not exist yet.
    """
    assert not PERF_REPORTS_LOGFILE.exists(), (
        f"Log file {PERF_REPORTS_LOGFILE} already exists, but it must be "
        "created by the student's command."
    )