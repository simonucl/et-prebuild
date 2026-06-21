# test_initial_state.py
#
# Pytest suite that verifies the machine is in a **clean** state
# before the student begins the “pen-test” exercise.

import os
from pathlib import Path

HOME = Path("/home/user")
PEN_TEST_DIR = HOME / "pen-test"
ENV_FILE = PEN_TEST_DIR / ".env"
REPORT_FILE = PEN_TEST_DIR / "scan_results.log"

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _assert_not_exists(path: Path):
    """
    Fail the test if the given path exists (file *or* directory).

    Parameters
    ----------
    path : pathlib.Path
        The absolute path whose non-existence is expected.
    """
    assert not path.exists(), (
        f"Pre-exercise check failed: '{path}' already exists.\n"
        "The working directory must start clean so the student can "
        "demonstrate the required creation steps."
    )

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_home_directory_exists_and_is_accessible():
    """Sanity-check that /home/user exists and is a directory."""
    assert HOME.exists(), "Expected base home directory '/home/user' is missing."
    assert HOME.is_dir(), "'/home/user' exists but is not a directory."

def test_pen_test_directory_absent():
    """The pen-test working directory must NOT exist yet."""
    _assert_not_exists(PEN_TEST_DIR)

def test_env_file_absent():
    """The .env file must NOT exist prior to the exercise."""
    _assert_not_exists(ENV_FILE)

def test_report_file_absent():
    """The scan_results.log file must NOT exist prior to the exercise."""
    _assert_not_exists(REPORT_FILE)

def test_environment_variables_not_set():
    """
    None of the required variables should be exported in the current
    shell environment before the student sources the .env file.
    """
    missing_vars = [
        var_name
        for var_name in (
            "TARGET_HOST",
            "TARGET_PORTS",
            "SCAN_TYPE",
            "REPORT_FILE",
            "AUTHOR",
        )
        if os.environ.get(var_name) is None
    ]

    assert len(missing_vars) == 5, (
        "One or more exercise-specific environment variables are already set: "
        f"{set(['TARGET_HOST','TARGET_PORTS','SCAN_TYPE','REPORT_FILE','AUTHOR']) - set(missing_vars)}\n"
        "The environment must start clean so the student can load them via the .env file."
    )