# test_initial_state.py
#
# This pytest suite verifies that the machine is still in its *pristine*
# state ­— i.e. the student has NOT yet created any part of the required
# diagnostic kit.  All checks must therefore PASS **only when** nothing
# related to `/home/user/system_monitor/` exists.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
MONITOR_DIR = HOME / "system_monitor"
RUN_DIAG = MONITOR_DIR / "run_diag.sh"
LATEST_REPORT = MONITOR_DIR / "latest_report.log"


def _pretty(p: Path) -> str:
    """Return a nicely-formatted absolute POSIX path for error messages."""
    return str(p.resolve())


@pytest.mark.parametrize(
    "path_obj, kind",
    [
        (MONITOR_DIR, "directory"),
        (RUN_DIAG, "file"),
        (LATEST_REPORT, "file"),
    ],
)
def test_monitor_assets_absent(path_obj: Path, kind: str):
    """
    Nothing related to the diagnostic kit should exist yet.

    This single parameterised test covers:
      • /home/user/system_monitor                (dir)
      • /home/user/system_monitor/run_diag.sh    (file)
      • /home/user/system_monitor/latest_report.log (file)

    If *any* of these pre-existing items are found, the test will fail with a
    clear, actionable message explaining what MUST NOT be present at the start
    of the exercise.
    """
    assert not path_obj.exists(), (
        f"Pre-flight check failed: the {kind} {_pretty(path_obj)} already "
        f"exists, but the exercise expects the learner to create it later.  "
        "Start with a clean slate."
    )


def test_no_stray_system_monitor_processes():
    """
    There should not be any long-running processes that already reference the
    `system_monitor` project (e.g. tailing the log, running a watch job, etc.).

    This check is intentionally lightweight and relies only on `/proc`.
    """
    proc_dir = Path("/proc")
    suspicious_procs = []

    for pid_dir in proc_dir.iterdir():
        if not pid_dir.name.isdigit():
            continue
        cmdline_file = pid_dir / "cmdline"
        try:
            cmdline = cmdline_file.read_text(errors="ignore")
        except (FileNotFoundError, PermissionError):
            # Process gone or not accessible; safely skip.
            continue
        if "system_monitor" in cmdline:
            suspicious_procs.append((pid_dir.name, cmdline.replace("\x00", " ")))

    assert not suspicious_procs, (
        "Found running processes that already reference 'system_monitor', "
        "which suggests the student has started work prematurely:\n"
        + "\n".join(f"PID {pid}: {cmd}" for pid, cmd in suspicious_procs)
    )


def test_home_directory_writable():
    """
    Sanity check: make sure /home/user is writable so the student can create
    the required files/directories later.  This is not part of the assignment
    itself, but guards against CI/container mis-configuration.
    """
    tmp_path = HOME / ".pytest_write_test"
    try:
        with open(tmp_path, "w") as fh:
            fh.write("ok")
    finally:
        # Clean up if the file happened to be created.
        if tmp_path.exists():
            tmp_path.unlink()

    # If we reached here without exceptions, writing was successful.
    assert True