# test_initial_state.py
"""
Pre-flight checks for the “LANG locale proof” exercise.

These tests verify that the filesystem is in its expected *initial*
state **before** the student performs any action.

Required initial state:
1. The directory  /home/user/capplan  must NOT exist.
2. Consequently, the file  /home/user/capplan/locale_check.log  must
   also be absent.

If any of these conditions fail, it means the environment has already
been modified and the exercise cannot be graded reliably.
"""

import os
from pathlib import Path
import pytest


CAPPLAN_DIR = Path("/home/user/capplan")
LOCALE_LOG = CAPPLAN_DIR / "locale_check.log"


def _pretty(path: Path) -> str:
    """Return a human-readable pathname enclosed in single quotes."""
    return f"'{str(path)}'"


def test_capplan_directory_absent():
    """
    Ensure that the directory /home/user/capplan does NOT exist yet.
    """
    assert not CAPPLAN_DIR.exists(), (
        f"The directory {_pretty(CAPPLAN_DIR)} already exists, but the "
        "exercise expects to create it. Remove or rename it before starting."
    )


def test_locale_log_absent():
    """
    Ensure that /home/user/capplan/locale_check.log is absent.
    This is a stricter check than the directory test so that, even if
    someone manually creates the directory, the presence of the file
    will still fail the test.
    """
    assert not LOCALE_LOG.exists(), (
        f"The file {_pretty(LOCALE_LOG)} already exists, but the exercise "
        "requires creating it as proof of setting LANG. Remove it first."
    )