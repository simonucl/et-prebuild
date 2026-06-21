# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system / filesystem
# state matches the specification provided to the student **before** they start
# working on the assignment.  These tests assert the presence, permissions and
# exact contents of all pre-existing resources that the solution relies on.
#
# IMPORTANT:
#   • We intentionally DO NOT test for the presence (or absence) of any output
#     artefacts the student is expected to create later (e.g.
#     /home/user/etl/reports/error_count.txt).  Only the initial inputs /
#     environment are checked here.

import os
import stat
import pytest
import textwrap

HOME = "/home/user"
LOG_DIR = os.path.join(HOME, "etl", "logs")
REPORT_DIR = os.path.join(HOME, "etl", "reports")
LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")


# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #
def _get_permissions(path):
    """
    Return Unix permission bits (e.g. 0o755, 0o644) for the given file/dir.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


def _read_file(path):
    """
    Read a text file using UTF-8, *without* universal newlines, so we can check
    for stray carriage-return characters.
    """
    with open(path, "r", encoding="utf-8", newline="") as fp:
        return fp.read()


# --------------------------------------------------------------------------- #
# Expected ground-truth values
# --------------------------------------------------------------------------- #
EXPECTED_LOG_CONTENT = [
    "[2023-05-12 08:00:01] INFO  Start extraction\n",
    "[2023-05-12 08:00:02] ERROR Source connection failure\n",
    "[2023-05-12 08:05:31] INFO  Retrying extraction\n",
    "[2023-05-12 08:05:45] INFO  Extraction succeeded\n",
    "[2023-05-12 08:06:00] INFO  Start transformation\n",
    "[2023-05-12 08:06:12] ERROR Null value encountered\n",
    "[2023-05-12 08:07:00] INFO  Transformation succeeded\n",
    "[2023-05-12 08:07:15] INFO  Start load\n",
    "[2023-05-12 08:07:45] ERROR Constraint violation on load\n",
    "[2023-05-12 08:08:02] INFO  Load finished\n",
]
GROUND_TRUTH_ERROR_COUNT = 3


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    """
    Both /home/user/etl/logs and /home/user/etl/reports must already exist with
    0755 permissions so that the student’s script can read / write as required.
    """
    for d in (LOG_DIR, REPORT_DIR):
        assert os.path.isdir(d), (
            f"Expected directory missing: {d!r}.  It must be present *before* "
            "the student runs their code."
        )
        perms = _get_permissions(d)
        assert perms == 0o755, (
            f"Directory {d!r} has permissions {oct(perms)}; expected 0o755 "
            "(rwxr-xr-x).  Please fix filesystem permissions."
        )


def test_pipeline_log_file_exists_and_permissions():
    """
    The log file that drives the task must exist with read-only (644) perms.
    """
    assert os.path.isfile(LOG_FILE), (
        f"Log file {LOG_FILE!r} is missing.  The assignment cannot be solved "
        "without it."
    )

    perms = _get_permissions(LOG_FILE)
    assert perms == 0o644, (
        f"{LOG_FILE!r} permissions are {oct(perms)}; expected 0o644 "
        "(rw-r--r--).  Please correct the file permissions."
    )


def test_pipeline_log_has_only_LF_line_endings():
    """
    The specification states the file uses LF line endings.  There must be no
    stray carriage-return characters.
    """
    data = _read_file(LOG_FILE)
    assert "\r" not in data, (
        f"{LOG_FILE!r} contains CR characters (Windows line endings).  "
        "It must use LF line endings only."
    )


def test_pipeline_log_exact_content():
    """
    Validate that the file contains exactly the expected ten lines.  Any drift
    here indicates the initial state is not what the student was told.
    """
    with open(LOG_FILE, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    assert lines == EXPECTED_LOG_CONTENT, textwrap.dedent(
        f"""
        The contents of {LOG_FILE!r} do not match the expected ground-truth
        lines.

        --- Expected (10 lines) ---
        {''.join(EXPECTED_LOG_CONTENT)}
        --- Got ({len(lines)} lines) ---
        {''.join(lines)}
        """
    ).strip()


def test_ground_truth_error_count():
    """
    Double-check the authoritative answer: there should be exactly three lines
    containing the exact token ' ERROR ' (one leading & one trailing space).
    """
    with open(LOG_FILE, "r", encoding="utf-8") as fp:
        error_lines = [
            ln for ln in fp
            if " ERROR " in ln  # Note: exact casing and spacing
        ]

    found = len(error_lines)
    assert found == GROUND_TRUTH_ERROR_COUNT, (
        f"Ground-truth mismatch: expected {GROUND_TRUTH_ERROR_COUNT} 'ERROR' "
        f"lines in {LOG_FILE!r}, but found {found}.  File contents may be "
        "corrupted or incomplete."
    )