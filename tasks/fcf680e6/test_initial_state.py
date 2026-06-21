# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating
# system / filesystem *before* the learner carries out the task.
#
# What we check
# -------------
# 1. The application directory /home/user/app exists.
# 2. The script /home/user/app/compute.sh exists and is executable.
# 3. The script, when executed, exits cleanly (status 0) and prints the
#    expected integer “5000050000”.
# 4. The profiling tool /usr/bin/time is present and executable.
#
# Nothing related to the eventual output directory /home/user/profile or
# its log file is verified here, in accordance with the instructions.

import os
import stat
import subprocess
from pathlib import Path

APP_DIR = Path("/home/user/app")
SCRIPT = APP_DIR / "compute.sh"
TIME_BIN = Path("/usr/bin/time")
EXPECTED_SUM = "5000050000"  # 1 + 2 + … + 100000


def test_app_directory_exists():
    assert APP_DIR.is_dir(), (
        f"Required directory {APP_DIR} is missing. "
        "Ensure the path exists before proceeding."
    )


def test_compute_script_exists_and_is_executable():
    assert SCRIPT.is_file(), (
        f"Required script {SCRIPT} is missing. "
        "It should already be present in the initial environment."
    )

    st_mode = SCRIPT.stat().st_mode
    is_executable = bool(st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"The script {SCRIPT} exists but is not marked executable. "
        "Run `chmod +x /home/user/app/compute.sh` to fix."
    )


def test_compute_script_outputs_expected_sum():
    """
    Run the script and ensure it produces the exact integer that the
    grading logic will later look for.  This guarantees the baseline
    behaviour is intact before any profiling is attempted.
    """
    completed = subprocess.run(
        [str(SCRIPT)],
        check=True,
        capture_output=True,
        text=True,
    )

    # Strip to remove the trailing newline, if any.
    output = completed.stdout.strip()

    assert output == EXPECTED_SUM, (
        f"The script {SCRIPT} ran but produced an unexpected result.\n"
        f"Expected: {EXPECTED_SUM!r}\n"
        f"Got     : {output!r}"
    )


def test_time_binary_available():
    assert TIME_BIN.is_file(), (
        "/usr/bin/time is required for profiling, but it is not present on "
        "this system. Install the 'time' package or adjust the path."
    )
    assert os.access(TIME_BIN, os.X_OK), (
        "/usr/bin/time exists but is not executable. "
        "Check its permissions."
    )