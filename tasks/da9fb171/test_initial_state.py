# test_initial_state.py
#
# Pytest test-suite that validates the **initial** state of the
# simulated CI filesystem before the student’s shell commands run.
#
# The checks intentionally avoid looking for any of the *output* artefacts
# the student is supposed to create (reports/, *.gz, …).  They only make
# sure that the prerequisite files, sizes and timestamps are in place.

import os
import stat
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants describing the ground-truth “starter” files.
# ---------------------------------------------------------------------------

HOME                  = Path("/home/user")
MOBILE_BUILD          = HOME / "mobile-build"
ARTIFACTS_DIR         = MOBILE_BUILD / "artifacts"
LOGS_DIR              = MOBILE_BUILD / "logs"

# Size threshold specified in the task (strictly greater than 20 MiB).
THRESHOLD_BYTES = 20 * 1024 * 1024  # 20 MiB → 20 971 520 bytes

# Expected artefact information: {filename: size_in_bytes}
EXPECTED_ARTIFACTS = {
    "app-debug-1.apk":  25 * 1024 * 1024,  # 25 MiB = 26 214 400 bytes
    "app-release.apk":  30 * 1024 * 1024,  # 30 MiB = 31 457 280 bytes
    "old-test.ipa":     28 * 1024 * 1024,  # 28 MiB = 29 360 128 bytes
    "beta-small.apk":   19 * 1024 * 1024,  # 19 MiB = 19 922 944 bytes (≤ threshold)
}

# Expected log files and whether they are supposed to be “old” (>7 days).
# Values:  True  → mtime must be strictly older than 7 days.
#          False → mtime must be newer than (or equal to) 7 days.
EXPECTED_LOGS = {
    "build-20230901.log": True,
    "test-20230902.log":  True,
    "build-latest.log":   False,
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_path(path: Path, what: str):
    """Fail with a helpful message if *path* does not exist."""
    assert path.exists(), f"Required {what} missing: {path!s}"

def _days_ago(days: int) -> float:
    """Return a POSIX timestamp corresponding to *days* ago from ‘now’."""
    return time.time() - (days * 24 * 60 * 60)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_artifacts_directory_exists():
    _assert_path(ARTIFACTS_DIR, "directory")
    assert ARTIFACTS_DIR.is_dir(), f"{ARTIFACTS_DIR} exists but is not a directory."


def test_expected_artifact_files_and_sizes():
    """
    • All four artefact files must exist at the exact absolute paths.
    • Their byte sizes must match the ground-truth values.
    • Additionally, verify which ones are above / below the 20 MiB threshold.
    """
    for fname, expected_size in EXPECTED_ARTIFACTS.items():
        fpath = ARTIFACTS_DIR / fname
        _assert_path(fpath, "artefact file")

        stat_info = fpath.stat()
        actual_size = stat_info.st_size
        assert actual_size == expected_size, (
            f"Size mismatch for {fpath}: expected {expected_size} bytes, "
            f"found {actual_size} bytes."
        )

        if expected_size > THRESHOLD_BYTES:
            assert actual_size > THRESHOLD_BYTES, (
                f"{fpath} should be strictly larger than 20 MiB."
            )
        else:
            assert actual_size <= THRESHOLD_BYTES, (
                f"{fpath} should be ≤ 20 MiB."
            )


def test_logs_directory_exists():
    _assert_path(LOGS_DIR, "directory")
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."


def test_expected_logs_exist_and_age():
    """
    • Verify each expected *.log file exists.
    • Check that its ‘oldness’ (mtime relative to now) matches EXPECTED_LOGS.
      “Old” means mtime < now − 7 days.
    """
    now = time.time()
    seven_days_ago = _days_ago(7)

    for fname, should_be_old in EXPECTED_LOGS.items():
        fpath = LOGS_DIR / fname
        _assert_path(fpath, "log file")
        assert fpath.is_file(), f"{fpath} is not a regular file."

        mtime = fpath.stat().st_mtime
        if should_be_old:
            assert mtime < seven_days_ago, (
                f"{fpath} ought to be older than 7 days but mtime is "
                f"{time.ctime(mtime)} which is too recent."
            )
        else:
            assert mtime >= seven_days_ago, (
                f"{fpath} is supposed to be *new* (≤7 days old) but mtime is "
                f"{time.ctime(mtime)} which is too old."
            )