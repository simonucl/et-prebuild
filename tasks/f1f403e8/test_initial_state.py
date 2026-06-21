# test_initial_state.py
#
# Pytest suite that verifies the container’s **initial** state for the
# “optimize_limits” exercise _before_ the student performs any action.
#
# Expectations:
#   1. Directory /home/user/security               … must exist.
#   2. File      /home/user/security/limits.csv    … must exist with exact contents.
#   3. The following paths must **NOT** exist yet:
#        • /home/user/security/optimize_limits.py
#        • /home/user/security/optimized_limits.csv
#        • /home/user/security/optimization_run.log
#
# Only the Python stdlib and pytest are used.

import os
from pathlib import Path

SECURITY_DIR = Path("/home/user/security")
LIMITS_CSV   = SECURITY_DIR / "limits.csv"
SCRIPT_PATH  = SECURITY_DIR / "optimize_limits.py"
OUTPUT_CSV   = SECURITY_DIR / "optimized_limits.csv"
LOG_FILE     = SECURITY_DIR / "optimization_run.log"


def test_security_directory_exists():
    assert SECURITY_DIR.is_dir(), (
        f"Required directory {SECURITY_DIR} is missing."
    )


def test_limits_csv_exists_and_exact_contents():
    assert LIMITS_CSV.is_file(), (
        f"Required file {LIMITS_CSV} is missing."
    )

    expected_bytes = (
        b"Parameter,Current\n"
        b"nofile,4096\n"
        b"nproc,8192\n"
        b"memlock,16384\n"
        b"fsize,1048576\n"
    )

    actual_bytes = LIMITS_CSV.read_bytes()
    assert actual_bytes == expected_bytes, (
        f"{LIMITS_CSV} contents do not match the expected initial CSV.\n"
        f"Expected (bytes):\n{expected_bytes!r}\n"
        f"Found (bytes):\n{actual_bytes!r}"
    )


def test_optimize_script_does_not_exist_yet():
    assert not SCRIPT_PATH.exists(), (
        f"{SCRIPT_PATH} should NOT exist before the student creates it."
    )


def test_optimized_limits_csv_absent_initially():
    assert not OUTPUT_CSV.exists(), (
        f"{OUTPUT_CSV} should NOT exist before the optimization is performed."
    )


def test_optimization_log_absent_initially():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist before the optimization is performed."
    )