# test_initial_state.py
#
# This pytest suite verifies the **initial** state of the filesystem *before*
# the learner performs any action.  It makes sure the required input assets are
# present and that none of the artefacts that the learner is expected to
# create already exist.
#
# NOTE: Do **not** modify this file.  It is executed by the automated grader.

import os
import stat
from pathlib import Path

HOME = Path("/home/user")
EXPERIMENTS_DIR = HOME / "experiments"
TOOLS_DIR = HOME / "tools"
LOGS_DIR = HOME / "logs"
README = EXPERIMENTS_DIR / "README.md"
LINTER = TOOLS_DIR / "md_lint.sh"
EXPECTED_LOG = LOGS_DIR / "experiments_lint.log"


def test_experiments_directory_exists():
    assert EXPERIMENTS_DIR.is_dir(), (
        f"Required directory '{EXPERIMENTS_DIR}' is missing. "
        "The experiments data must be present before running the task."
    )


def test_tools_directory_exists():
    assert TOOLS_DIR.is_dir(), (
        f"Required directory '{TOOLS_DIR}' is missing. "
        "The Markdown linter script must reside here."
    )


def test_readme_exists_and_is_file():
    assert README.is_file(), (
        f"Required README file '{README}' is missing. "
        "The linter cannot be executed without this file."
    )


def test_linter_exists_and_is_executable():
    assert LINTER.is_file(), f"Linter script '{LINTER}' is missing."
    st_mode = LINTER.stat().st_mode
    is_executable = bool(st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"Linter script '{LINTER}' is not executable. "
        "It must have its executable bit set."
    )


def test_logs_directory_does_not_exist_yet():
    assert not LOGS_DIR.exists(), (
        f"Directory '{LOGS_DIR}' already exists but should be created by "
        "the learner's solution, not beforehand."
    )


def test_expected_log_file_does_not_exist():
    assert not EXPECTED_LOG.exists(), (
        f"Log file '{EXPECTED_LOG}' already exists. "
        "The learner's solution is supposed to generate this file."
    )