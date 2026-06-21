# test_initial_state.py
"""
Pytest suite that validates the operating system / filesystem **before** the
student performs any actions for the “pip-health” incident-report task.

Verification goals _before_ the student solution runs:
1. The machine has a `/home/user` directory (base workspace).
2. The system-level Python installation can execute
   `python -m pip check` **cleanly**, proving there are _no_ dependency
   conflicts at the outset.  This guarantees the expected output the student
   must later capture in `/home/user/incident_reports/pip_health.log`.

Notes / rules respected:
• We do **not** assert anything about `/home/user/incident_reports`
  or the `pip_health.log` file, because those are artefacts that will only be
  created by the student solution (rule: “DO NOT test for any of the output
  files or directories”).
• Only stdlib + pytest are used.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def home_path() -> Path:
    """Return the canonical Path object for /home/user ."""
    return Path("/home/user")


def test_home_directory_exists(home_path: Path):
    """
    The base workspace directory for the student must be present _before_
    they begin.  If it is absent the entire exercise breaks, so we fail fast
    with a clear message.
    """
    assert home_path.exists(), f"Required directory not found: {home_path}"
    assert home_path.is_dir(), f"Expected a directory at {home_path}, but found something else."


def test_pip_check_reports_clean_environment():
    """
    Ensure that the active, system-level Python environment is already free
    of dependency conflicts.  The student will later re-run the exact same
    command and store its output; therefore, it must succeed right now.

    The canonical success output for `pip check` is the single line:
        'No broken requirements found.\\n'
    """
    result = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        capture_output=True,
        text=True,
        check=False,
    )

    # 1. The command must complete successfully (exit status 0).
    assert (
        result.returncode == 0
    ), f"`pip check` exited with status {result.returncode}. stderr was:\n{result.stderr}"

    expected_stdout = "No broken requirements found.\n"

    # 2. The output must match exactly; no extra whitespace or lines.
    assert (
        result.stdout == expected_stdout
    ), (
        "System-wide packages report dependency problems or unexpected output.\n"
        f"Expected stdout:\n    {expected_stdout!r}\n"
        f"Actual stdout:\n    {result.stdout!r}"
    )

    # 3. stderr should be empty for a clean environment.
    assert (
        result.stderr == ""
    ), f"`pip check` produced output on stderr unexpectedly:\n{result.stderr}"