# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem *before* the learner starts the exercise described in the
# instructions.  If any of these tests fail, the environment is **not** in the
# expected pristine state and the learner might get misleading feedback.

import os
import subprocess
from pathlib import Path

import pytest

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
HOME = Path("/home/user")
DOC_DIR = HOME / "documentation"
PROC_MGMT_DIR = DOC_DIR / "process_mgmt"
PROCESS_MD = PROC_MGMT_DIR / "process_overview.md"
SIGNAL_LOG = PROC_MGMT_DIR / "signal_audit.log"

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def _get_user_process_args():
    """
    Return a list of command-line strings (ARGS column) for all processes
    owned by the current user.
    """
    try:
        result = subprocess.run(
            ["ps", "-u", os.getlogin(), "-o", "args="],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        # Fallback if os.getlogin() fails (e.g., inside some CI containers)
        result = subprocess.run(
            ["ps", "-u", str(os.getuid()), "-o", "args="],
            check=True,
            capture_output=True,
            text=True,
        )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_process_management_directory_absent():
    """
    The directory /home/user/documentation/process_mgmt *must not* exist yet.
    A learner should create it during the exercise.
    """
    assert not PROC_MGMT_DIR.exists(), (
        f"Directory {PROC_MGMT_DIR} already exists. "
        "The initial state should not contain this directory."
    )


def test_documentation_parent_directory_may_exist():
    """
    The parent /home/user/documentation is allowed to exist (it may contain
    unrelated material), but it must *not* already have the process_mgmt child.
    """
    if DOC_DIR.exists():
        assert PROC_MGMT_DIR not in DOC_DIR.iterdir(), (
            "/home/user/documentation exists but already contains a "
            "process_mgmt sub-directory.  The learner must create it."
        )


@pytest.mark.parametrize("path_obj,description", [
    (PROCESS_MD, "process_overview.md"),
    (SIGNAL_LOG, "signal_audit.log"),
])
def test_no_task_files_present(path_obj: Path, description: str):
    """
    Neither the Markdown overview file nor the signal log should exist
    at the beginning of the task.
    """
    assert not path_obj.exists(), (
        f"{description} ({path_obj}) is present before the learner has started. "
        "The initial state must not contain this file."
    )


def test_no_helper_processes_running():
    """
    Ensure that the helper commands ('sleep 1000' and the specialised
    'yes' command) are not already running for the current user.
    """
    offending = []
    for args in _get_user_process_args():
        if "sleep 1000" in args:
            offending.append(args)
        elif args.startswith("yes") and "Compiling docs" in args:
            offending.append(args)

    assert not offending, (
        "The following helper processes are already running but should not be "
        f"in the initial state:\n{chr(10).join(offending)}"
    )