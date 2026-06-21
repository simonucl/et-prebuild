# test_initial_state.py
#
# Pytest test-suite that verifies the *pre-exercise* state of the host.
# It checks that only the starting artefacts are present and that no
# traces of the solution (profile_logs/, running cpu_hog.py processes,
# etc.) exist yet.

import os
import stat
import subprocess
import textwrap
from pathlib import Path

APPS_DIR = Path("/home/user/apps")
CPU_HOG = APPS_DIR / "cpu_hog.py"
PROFILE_DIR = Path("/home/user/profile_logs")
PROFILE_LOG = PROFILE_DIR / "app_profile.log"


def test_apps_directory_exists():
    assert APPS_DIR.is_dir(), (
        f"Required directory {APPS_DIR} is missing.\n"
        "Create it exactly at that absolute path."
    )


def test_cpu_hog_file_exists_and_is_correct():
    assert CPU_HOG.is_file(), (
        f"Expected file {CPU_HOG} does not exist.\n"
        "It must already be present before you begin."
    )

    # Check that the file is user-executable.
    assert os.access(CPU_HOG, os.X_OK), (
        f"File {CPU_HOG} exists but is not executable (missing +x)."
    )

    # Verify file contents match the specification exactly.
    expected_content = textwrap.dedent(
        """\
        #!/usr/bin/env python3
        import math, time
        while True:
            x = math.sqrt(98765.4321) ** 2      # pointless calculation
        """
    )
    with CPU_HOG.open("r", encoding="utf-8") as fp:
        actual_content = fp.read()

    assert actual_content == expected_content, (
        f"Contents of {CPU_HOG} do not match the required template.\n"
        "Make sure the file has not been modified."
    )


def test_profile_logs_not_present_yet():
    """
    Before the student does any work, the profiling directory and log file
    should NOT exist.  Their presence would indicate the final artefacts have
    been created prematurely.
    """
    assert not PROFILE_LOG.exists(), (
        f"{PROFILE_LOG} already exists; it should be created only after the "
        "profiling script has run."
    )
    # The directory itself must also be absent (or at least empty of the log).
    if PROFILE_DIR.exists():
        assert PROFILE_DIR.is_dir(), f"{PROFILE_DIR} exists but is not a directory."


def test_no_cpu_hog_process_running():
    """
    Ensure there are currently NO running processes that match cpu_hog.py.
    """
    result = subprocess.run(
        ["pgrep", "-f", "cpu_hog.py"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1, (
        "Found running cpu_hog.py processes before the exercise started:\n"
        f"{result.stdout.strip()}\n"
        "Make sure no leftovers are running."
    )