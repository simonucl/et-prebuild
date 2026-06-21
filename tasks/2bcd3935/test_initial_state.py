# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present before the student executes any commands.  If any of these tests
# fail, it means the sandbox is not set up the way the task expects and the
# assessment will be unreliable.

import os
from pathlib import Path

IAC_DIR = Path("/home/user/iac")
MAIN_TF = IAC_DIR / "main.tf"
DB_TF = IAC_DIR / "db.tf"
VARS_TF = IAC_DIR / "variables.tf"
SCAN_RESULTS = Path("/home/user/scan_results.log")


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _read_lines(path: Path):
    """
    Read a file and return its lines *exactly as stored on disk*
    (including trailing whitespace, minus the final newline) so that we
    can make strict, character-for-character assertions.
    """
    with path.open("r", encoding="utf-8") as f:
        # .splitlines(keepends=False) preserves all characters except '\n'
        return f.read().splitlines(keepends=False)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_iac_directory_exists_and_is_directory():
    assert IAC_DIR.exists(), f"Expected directory {IAC_DIR} to exist."
    assert IAC_DIR.is_dir(), f"Expected {IAC_DIR} to be a directory."


def test_expected_tf_files_exist():
    for tf_file in (MAIN_TF, DB_TF, VARS_TF):
        assert tf_file.exists(), f"Expected file {tf_file} to exist."
        assert tf_file.is_file(), f"Expected {tf_file} to be a regular file."


def test_main_tf_contents_exact():
    expected = [
        'resource "aws_security_group" "web" {',
        '  name = "web"',
        '  ingress {',
        '    from_port   = 80',
        '    to_port     = 80',
        '    protocol    = "tcp"',
        '    cidr_blocks = ["0.0.0.0/0"]',
        '  }',
        '}',
    ]
    actual = _read_lines(MAIN_TF)
    assert actual == expected, (
        f"File {MAIN_TF} does not match the expected contents.\n"
        f"Expected ({len(expected)} lines):\n{expected}\n\n"
        f"Actual ({len(actual)} lines):\n{actual}"
    )


def test_db_tf_contents_exact():
    expected = [
        'resource "aws_security_group" "db" {',
        '  name = "db"',
        '  ingress {',
        '    from_port   = 5432',
        '    to_port     = 5432',
        '    protocol    = "tcp"',
        '    cidr_blocks = ["10.0.0.0/16"]',
        '  }',
        '  egress {',
        '    from_port   = 0',
        '    to_port     = 0',
        '    protocol    = "-1"',
        '    cidr_blocks = ["0.0.0.0/0"]',
        '  }',
        '}',
    ]
    actual = _read_lines(DB_TF)
    assert actual == expected, (
        f"File {DB_TF} does not match the expected contents.\n"
        f"Expected ({len(expected)} lines):\n{expected}\n\n"
        f"Actual ({len(actual)} lines):\n{actual}"
    )


def test_variables_tf_is_empty():
    size = VARS_TF.stat().st_size
    assert size == 0, f"Expected {VARS_TF} to be an empty file, but it is {size} bytes."


def test_scan_results_log_absent_initially():
    assert not SCAN_RESULTS.exists(), (
        f"{SCAN_RESULTS} should NOT exist before the student runs their "
        "command.  The grading suite expects the student to create it."
    )