# test_initial_state.py
"""
Pre-flight checks for the “QA harness” exercise.

These tests are meant to be executed **before** the student performs any of the
required steps.  They make sure the filesystem is still in its pristine state.
If any of these tests fail it means the student (or a previous run) has already
created artefacts that should not exist yet.

Expected _absence_ at this point:
1. /home/user/qa_env/                  – the workspace directory
2. /home/user/qa_env/test_sample.py   – the sample test file
3. /home/user/qa_env/venv/            – the virtual environment
4. /home/user/qa_test_results.log     – the test run log
"""

import os
from pathlib import Path

HOME = Path("/home/user")
QA_ENV_DIR = HOME / "qa_env"
TEST_FILE = QA_ENV_DIR / "test_sample.py"
VENV_DIR = QA_ENV_DIR / "venv"
LOG_FILE = HOME / "qa_test_results.log"


def _assert_absent(path: Path):
    """
    Helper that asserts a given path (file or directory) does **not** exist.
    Produces a clear pytest assertion message on failure.
    """
    assert not path.exists(), f"'{path}' already exists but should NOT be present before the exercise starts."


def test_workspace_directory_absent():
    """The workspace directory must not exist yet."""
    _assert_absent(QA_ENV_DIR)


def test_sample_test_file_absent():
    """The test_sample.py file must not exist yet."""
    _assert_absent(TEST_FILE)


def test_virtualenv_absent():
    """The virtual environment directory must not exist yet."""
    _assert_absent(VENV_DIR)


def test_log_file_absent():
    """The qa_test_results.log file must not exist yet."""
    _assert_absent(LOG_FILE)