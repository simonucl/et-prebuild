# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the container
# before the student performs any action for the “system snapshot”
# task.  These tests confirm that
#
# 1.  The diagnostics artefacts the student must create are **absent**.
# 2.  The operating-system resources needed to complete the task are
#     present and working.
#
# Only the Python standard library and pytest are used.

import os
import subprocess
import sys
from pathlib import Path

import pytest

HOME_DIR = Path("/home/user")
DIAG_DIR = HOME_DIR / "diagnostics"
SNAPSHOT_FILE = DIAG_DIR / "system_snapshot.log"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    """
    Run *cmd* and return the CompletedProcess.  The command must succeed.
    """
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


# ---------------------------------------------------------------------------
# Tests related to the pre-existing diagnostics artefacts
# ---------------------------------------------------------------------------


def test_diagnostics_directory_absent_or_clean():
    """
    The diagnostics directory should **not** exist yet.  If it does exist
    (left over from some unrelated process), it must be a directory and must
    NOT already contain the snapshot file the student is supposed to create.
    """
    if not DIAG_DIR.exists():
        # Ideal, clean starting point.
        return

    # If the path exists it must be a directory, not a file.
    assert DIAG_DIR.is_dir(), (
        f"{DIAG_DIR} exists but is not a directory.  Remove or rename it "
        "before starting the exercise."
    )

    # Ensure the target file is not already present.
    assert not SNAPSHOT_FILE.exists(), (
        f"{SNAPSHOT_FILE} already exists.  The snapshot must be created by "
        "the student; remove the file to start with a clean slate."
    )


def test_snapshot_file_does_not_exist():
    """
    The snapshot file itself must be absent at the beginning of the task.
    """
    assert not SNAPSHOT_FILE.exists(), (
        f"{SNAPSHOT_FILE} is already present.  The student should create this "
        "file as part of the exercise; remove it to reset the environment."
    )


# ---------------------------------------------------------------------------
# Tests that ensure required system resources/commands are available
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path, description",
    [
        (Path("/etc/os-release"), "/etc/os-release must exist so OS_NAME can be read"),
        (Path("/proc/meminfo"), "/proc/meminfo must exist so MEM_AVAILABLE_MB can be read"),
    ],
)
def test_required_files_present(path: Path, description: str):
    assert path.exists(), f"Required file {path} is missing: {description}"
    assert path.is_file(), f"Required path {path} exists but is not a regular file."


@pytest.mark.parametrize(
    "command, args, desc",
    [
        ("uname", ["-r"], "`uname -r` required for KERNEL_VERSION"),
        ("uptime", ["-p"], "`uptime -p` required for UPTIME"),
        ("df", ["-h", "/"], "`df -h /` required for ROOT_DISK_USAGE"),
        ("ss", ["-tln"], "`ss -tln` required for TCP_LISTEN_PORTS"),
    ],
)
def test_required_commands_work(command: str, args: list[str], desc: str):
    """
    Verify that each external command needed for the task is available and
    executes successfully with its intended arguments.
    """
    try:
        result = _run([command, *args])
    except FileNotFoundError:
        pytest.fail(f"Required command '{command}' is not installed ({desc}).")
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Command '{command} {' '.join(args)}' failed with exit code "
            f"{exc.returncode} ({desc}). StdErr: {exc.stderr.strip()}"
        )

    # Basic sanity check: the command produced *some* output.
    assert result.stdout.strip(), (
        f"Command '{command} {' '.join(args)}' produced no output ({desc})."
    )


def test_python_version_sufficient():
    """
    A reasonably recent Python (3.8+) is assumed by many learners.  Confirm it.
    """
    major, minor = sys.version_info[:2]
    assert (major, minor) >= (3, 8), (
        f"Python >= 3.8 is required; found {major}.{minor}.  "
        "Upgrade the environment before continuing."
    )