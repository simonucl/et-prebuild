# test_initial_state.py
#
# Pytest suite that validates the pre-populated operating-system state *before*
# the student executes any command.  It checks only the scaffolding that must
# already be in place and deliberately ignores the artefacts that the student
# will create later.

import os
import time
from pathlib import Path

# Fixed absolute paths used throughout the tests
LOG_ROOT = Path("/home/user/app/logs")
OLD_LOG_DIR = LOG_ROOT / "old"
DIAG_DIR = Path("/home/user/diag")

SERVICE_A = LOG_ROOT / "serviceA.log"
SERVICE_B = LOG_ROOT / "serviceB.log"
SERVICE_C = OLD_LOG_DIR / "serviceC.log"
DEBUG_TXT = LOG_ROOT / "debug.txt"

NOW = time.time()


def _assert_file(path: Path):
    """Helper that fails with a clear message if *path* is not an existing file."""
    assert path.exists(), f"Expected file {path} to exist, but it does not."
    assert path.is_file(), f"Expected {path} to be a file, but it is not."


def _assert_dir(path: Path):
    """Helper that fails with a clear message if *path* is not an existing directory."""
    assert path.exists(), f"Expected directory {path} to exist, but it does not."
    assert path.is_dir(), f"Expected {path} to be a directory, but it is not."


def test_log_directory_structure():
    """The log tree and the old-logs subdirectory must already exist."""
    _assert_dir(LOG_ROOT)
    _assert_dir(OLD_LOG_DIR)


def test_required_log_files_exist_and_sizes_are_correct():
    """Each of the three .log files (and debug.txt) must exist with the exact sizes."""
    _assert_file(SERVICE_A)
    _assert_file(SERVICE_B)
    _assert_file(SERVICE_C)
    _assert_file(DEBUG_TXT)

    # Exact byte sizes expected for the pre-seeded fixtures
    expected_sizes = {
        SERVICE_A: 153_600,
        SERVICE_B: 81_920,
        SERVICE_C: 307_200,
    }
    for path, expected in expected_sizes.items():
        actual = path.stat().st_size
        assert (
            actual == expected
        ), f"Size mismatch for {path}: expected {expected} bytes, found {actual}."

    # debug.txt is deliberately small (<10 KiB) and irrelevant
    debug_size = DEBUG_TXT.stat().st_size
    assert (
        debug_size < 10 * 1024
    ), f"{DEBUG_TXT} should be a small helper file (<10 KiB), but is {debug_size} bytes."


def test_log_file_ages():
    """
    Verify modification times so that subsequent tests about
    'recent' / 'old' are meaningful.
    """
    two_days = 2 * 24 * 60 * 60
    seven_days = 7 * 24 * 60 * 60

    # serviceA.log and serviceB.log must both be newer than 2 days.
    for path in (SERVICE_A, SERVICE_B):
        age = NOW - path.stat().st_mtime
        assert (
            0 < age < two_days
        ), f"{path} should be <2 days old, but its age is {age/3600:.2f} h."

    # serviceC.log must be at least 7 days old.
    age_c = NOW - SERVICE_C.stat().st_mtime
    assert (
        age_c > seven_days
    ), f"{SERVICE_C} should be >7 days old, but its age is {age_c/3600:.2f} h."


def test_diag_directory_is_present_and_empty():
    """
    The destination directory for the student's artefacts must already exist,
    but it must be completely empty before any work begins.
    """
    _assert_dir(DIAG_DIR)
    contents = list(DIAG_DIR.iterdir())
    assert (
        not contents
    ), f"{DIAG_DIR} is expected to be empty, but contains: {[p.name for p in contents]}"