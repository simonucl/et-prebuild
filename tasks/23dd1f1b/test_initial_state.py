# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem state
# *before* the learner performs any housekeeping / compression work.
#
# IMPORTANT:
# • These tests are intentionally strict; they make sure the sandbox starts from the
#   exact conditions described in the assignment statement so that the student can
#   rely on them when writing the housekeeping script.
# • ONLY the Python standard library and pytest are used.
# • Wherever a failure can occur, a clear and actionable message is emitted.

import os
import stat
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants – keep all hard-coded paths in one place for easier maintenance
# ---------------------------------------------------------------------------

HOME = Path("/home/user")

# Project tree
P_BENCH = HOME / "projects" / "benchmarks"

PERF_OLD_1 = P_BENCH / "app1" / "profiles" / "2023-01-15_run1.perf"
PERF_OLD_2 = P_BENCH / "app2" / "perf_logs" / "performance.perf"
PERF_OLD_3 = P_BENCH / "legacy" / "old_perf.perf"
PERF_NEW   = P_BENCH / "newapp" / "newrun.perf"

NON_PERF   = P_BENCH / "app1" / "readme.txt"

# Corresponding “.gz” targets that must **not** yet exist
GZ_1 = PERF_OLD_1.with_suffix(PERF_OLD_1.suffix + ".gz")
GZ_2 = PERF_OLD_2.with_suffix(PERF_OLD_2.suffix + ".gz")
GZ_3 = PERF_OLD_3.with_suffix(PERF_OLD_3.suffix + ".gz")

# Log-file related paths
ARCHIVAL_DIR  = HOME / "archival_logs"
SUMMARY_LOG   = ARCHIVAL_DIR / "compression_summary.log"

# Time window definitions
SECONDS_PER_DAY     = 24 * 60 * 60
DAYS_THRESHOLD      = 30
THIRTY_DAYS_SECONDS = DAYS_THRESHOLD * SECONDS_PER_DAY
NOW_TS = time.time()

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _assert_exists(path: Path, is_file=True):
    assert path.exists(), f"Expected path to exist: {path}"
    if is_file:
        assert path.is_file(), f"Expected a regular file at {path}, but found otherwise."
    else:
        assert path.is_dir(), f"Expected a directory at {path}, but found otherwise."

def _assert_not_exists(path: Path):
    assert not path.exists(), f"Path should NOT exist yet (will be created by student): {path}"

def _get_mtime(path: Path) -> float:
    return path.stat().st_mtime


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_files_exist_with_correct_types():
    """
    All files/directories promised by the task MUST already exist,
    and they must be of the correct type (file vs directory).
    """
    # Existing '.perf' files
    for perf_path in (PERF_OLD_1, PERF_OLD_2, PERF_OLD_3, PERF_NEW):
        _assert_exists(perf_path)

    # Non-.perf readme file
    _assert_exists(NON_PERF)

    # The archival directory should already exist so students can write the summary
    _assert_exists(ARCHIVAL_DIR, is_file=False)


def test_no_compressed_files_or_summary_log_exist_yet():
    """
    Ensure the sandbox is truly in the *pre-compression* state:
    • No '.gz' versions of the files are present.
    • No summary log has been created yet.
    """
    for gz_path in (GZ_1, GZ_2, GZ_3):
        _assert_not_exists(gz_path)

    _assert_not_exists(SUMMARY_LOG)


def test_old_perf_files_are_older_than_threshold():
    """
    The three 'old' .perf files *must* have mtimes strictly older than 30 days,
    because the student script is supposed to pick them up for compression.
    """
    for perf_path in (PERF_OLD_1, PERF_OLD_2, PERF_OLD_3):
        mtime = _get_mtime(perf_path)
        age_seconds = NOW_TS - mtime
        assert age_seconds > THIRTY_DAYS_SECONDS, (
            f"File {perf_path} should be older than {DAYS_THRESHOLD} days "
            f"but appears to be only {age_seconds/SECONDS_PER_DAY:.2f} days old."
        )


def test_new_perf_file_is_recent():
    """
    The single 'new' .perf file must *not* be older than 30 days so that the
    housekeeping script leaves it untouched.
    """
    mtime = _get_mtime(PERF_NEW)
    age_seconds = NOW_TS - mtime
    assert age_seconds <= THIRTY_DAYS_SECONDS, (
        f"File {PERF_NEW} should be ≤ {DAYS_THRESHOLD} days old so it is NOT "
        "compressed, but it appears older."
    )


def test_non_perf_file_left_alone():
    """
    The presence of a non-'.perf' file confirms that the directory housing rule
    is realistic and not all files share the '.perf' suffix.
    """
    _assert_exists(NON_PERF)
    # Ensure it is not a symlink, device, etc. Must be a regular file.
    mode = NON_PERF.stat().st_mode
    assert stat.S_ISREG(mode), f"Expected {NON_PERF} to be a regular file."