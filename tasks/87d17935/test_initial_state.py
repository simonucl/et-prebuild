# test_initial_state.py
"""
Pytest test-suite that validates the *initial* state of the workstation
_before_ the student begins to work on the “archive experiments” task.

The tests assert that
1. The required base directories exist.
2. /home/user/experiments contains exactly the expected test artefacts.
3. All artefacts in /home/user/experiments are strictly older than seven days.
4. /home/user/archive and /home/user/logs are empty.
5. The helper script /home/user/bin/archive_experiments.sh does NOT yet exist.

If any of these pre-conditions fail, the subsequent evaluation of the
student’s solution would be meaningless, so we stop early with an
informative error message.
"""
import os
import stat
import time
from pathlib import Path

import pytest

HOME = Path("/home/user")
EXP_DIR = HOME / "experiments"
ARCHIVE_DIR = HOME / "archive"
LOGS_DIR = HOME / "logs"
BIN_DIR = HOME / "bin"
SCRIPT_PATH = BIN_DIR / "archive_experiments.sh"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _list_all_paths(directory: Path):
    """Return a set of all (recursive) paths inside *directory*."""
    return {p for p in directory.rglob("*") if p.name != ""}


def _mtime_is_older_than(path: Path, seconds: int) -> bool:
    """Return True if *path*'s mtime is older than *seconds* seconds."""
    return (time.time() - path.stat().st_mtime) > seconds


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_base_directories_exist():
    """
    Ensure that the four base directories are present and are directories.
    """
    for d in (EXP_DIR, ARCHIVE_DIR, LOGS_DIR, BIN_DIR):
        assert d.exists(), f"Required directory {d} is missing."
        assert d.is_dir(), f"{d} exists but is not a directory."


def test_experiments_expected_content():
    """
    The /home/user/experiments directory must contain exactly three
    top-level entries with the given names and structure.

      /home/user/experiments/exp_alpha/model.bin
      /home/user/experiments/exp_beta/model.chk
      /home/user/experiments/exp_gamma/metrics.json
    """
    expected = {
        EXP_DIR / "exp_alpha",
        EXP_DIR / "exp_alpha" / "model.bin",
        EXP_DIR / "exp_beta",
        EXP_DIR / "exp_beta" / "model.chk",
        EXP_DIR / "exp_gamma",
        EXP_DIR / "exp_gamma" / "metrics.json",
    }

    actual = _list_all_paths(EXP_DIR)

    # For readability in an assertion error we convert to sorted lists
    missing = sorted(str(p) for p in expected - actual)
    unexpected = sorted(str(p) for p in actual - expected)

    assert not missing, (
        "The following expected files/directories are missing from "
        f"{EXP_DIR}:\n  " + "\n  ".join(missing)
    )
    assert not unexpected, (
        "Found unexpected files/directories in "
        f"{EXP_DIR}:\n  " + "\n  ".join(unexpected)
    )


def test_experiments_items_are_older_than_seven_days():
    """
    Every item inside /home/user/experiments must have a modification time
    strictly older than seven days.
    """
    SEVEN_DAYS = 7 * 24 * 60 * 60  # seconds

    failures = []
    for path in _list_all_paths(EXP_DIR):
        if not _mtime_is_older_than(path, SEVEN_DAYS):
            age_hours = (time.time() - path.stat().st_mtime) / 3600
            failures.append(f"{path} is only {age_hours:.2f} h old")

    assert not failures, (
        "The following artefacts are not older than seven days:\n  "
        + "\n  ".join(failures)
    )


def test_archive_and_logs_are_empty():
    """
    Both /home/user/archive and /home/user/logs must start out empty so that
    the student script can create new files there.
    """
    for directory in (ARCHIVE_DIR, LOGS_DIR):
        contents = sorted(directory.iterdir())
        assert not contents, (
            f"{directory} is expected to be empty at the beginning, but "
            f"contains {len(contents)} item(s): "
            + ", ".join(str(p.name) for p in contents)
        )


def test_script_does_not_exist_yet():
    """
    The helper script must NOT exist before the student creates it.
    """
    assert not SCRIPT_PATH.exists(), (
        f"{SCRIPT_PATH} already exists. The test harness expects the student "
        "to create this file as part of the task."
    )