# test_initial_state.py
#
# This test-suite asserts the pristine filesystem state that must exist
# *before* the student runs any command.  It verifies:
#   • Required directories and regular files are present.
#   • Exactly four “*.bak” files exist beneath /home/user/project.
#   • /home/user/cleanup_log.txt does NOT yet exist.
#
# The tests purposefully do NOT look for any post-command artefacts.

import os
import stat
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project").resolve()
EXPECTED_DIRECTORIES = [
    PROJECT_ROOT,
    PROJECT_ROOT / "src",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "tmp",
]

# Files that must be present and kept (non-.bak).
EXPECTED_REGULAR_FILES = [
    PROJECT_ROOT / "src" / "main.c",
    PROJECT_ROOT / "src" / "util.c",
    PROJECT_ROOT / "docs" / "readme.md",
    PROJECT_ROOT / "tmp" / "notes.txt",
    PROJECT_ROOT / "tmp" / "old.tmp",
]

# “*.bak” files that are supposed to exist *before* cleanup.
EXPECTED_BAK_FILES = [
    PROJECT_ROOT / "src" / "main.c.bak",
    PROJECT_ROOT / "src" / "util.c.bak",
    PROJECT_ROOT / "docs" / "readme.md.bak",
    PROJECT_ROOT / "tmp" / "notes.txt.bak",
]

CLEANUP_LOG = Path("/home/user/cleanup_log.txt")


def _assert_is_regular(path: Path):
    """Helper: assert path is a regular file."""
    assert path.exists(), f"Expected file {path} to exist, but it is missing."
    st_mode = path.stat().st_mode
    assert stat.S_ISREG(st_mode), f"Expected {path} to be a regular file."


def test_required_directories_exist():
    """Verify that every required directory exists and is a directory."""
    for dpath in EXPECTED_DIRECTORIES:
        assert dpath.exists(), f"Directory {dpath} is missing."
        assert dpath.is_dir(), f"{dpath} exists but is not a directory."


def test_required_regular_files_exist():
    """Verify that every non-.bak file exists and is a regular file."""
    for fpath in EXPECTED_REGULAR_FILES:
        _assert_is_regular(fpath)


def test_bak_files_exist_and_only_those():
    """
    There must be exactly four .bak files under the project tree and they must
    be precisely the ones listed in EXPECTED_BAK_FILES.
    """
    found_baks = sorted(str(p) for p in PROJECT_ROOT.rglob("*.bak"))
    expected_baks = sorted(str(p) for p in EXPECTED_BAK_FILES)

    assert found_baks, "No .bak files were found; 4 were expected."
    assert found_baks == expected_baks, (
        "The set of .bak files under the project tree does not match the "
        "expected initial state.\n"
        f"Expected:\n  " + "\n  ".join(expected_baks) + "\n"
        f"Found:\n  " + "\n  ".join(found_baks)
    )

    # Sanity-check each listed .bak file is a regular file.
    for fpath in EXPECTED_BAK_FILES:
        _assert_is_regular(fpath)


def test_cleanup_log_does_not_exist_yet():
    """The log file should not be present before the student runs the command."""
    assert not CLEANUP_LOG.exists(), (
        f"{CLEANUP_LOG} already exists; it should be created only by the "
        "cleanup command."
    )