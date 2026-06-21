# test_initial_state.py
"""
Pytest suite that validates the on-disk state *before* the student starts
working on the assignment.

These tests assert the following pre-conditions:

1. Directory layout
   • /home/user/project/                 — must exist, mode 0700
   • /home/user/project/artifacts/       — must exist, mode 0700
   • /home/user/project/reports/         — MUST NOT exist yet

2. Seed data file
   • /home/user/project/artifacts/list.txt
       – must exist as a regular file
       – mode 0644
       – must contain exactly the 13 expected lines (LF-terminated)

Any deviation will cause a failure with an explanatory message.
"""
import os
import stat
import pytest

# ---------- Constants -------------------------------------------------------

PROJECT_DIR      = "/home/user/project"
ARTIFACTS_DIR    = "/home/user/project/artifacts"
REPORTS_DIR      = "/home/user/project/reports"
LIST_TXT         = "/home/user/project/artifacts/list.txt"

EXPECTED_LIST_LINES = [
    "artifact-alpha-1.0.0.jar\n",
    "artifact-beta-2.1.0.jar\n",
    "artifact-alpha-1.0.0.jar\n",
    "artifact-gamma-3.3.7.jar\n",
    "artifact-alpha-1.0.0.jar\n",
    "artifact-beta-2.1.0.jar\n",
    "artifact-delta-4.0.0.jar\n",
    "artifact-epsilon-5.2.1.jar\n",
    "artifact-gamma-3.3.7.jar\n",
    "artifact-gamma-3.3.7.jar\n",
    "artifact-beta-2.1.0.jar\n",
    "artifact-delta-4.0.0.jar\n",
    "artifact-beta-2.1.0.jar\n",
]

# ---------- Helper utilities ------------------------------------------------


def _assert_path_mode(path: str, expected_octal: int):
    """
    Assert that `path` has permissions exactly equal to `expected_octal`
    (masking off the upper bits so that only the permission bits are compared).
    """
    st_mode = os.stat(path).st_mode
    actual = stat.S_IMODE(st_mode)
    assert actual == expected_octal, (
        f"Expected permissions {oct(expected_octal)} for {path}, "
        f"but found {oct(actual)}."
    )


# ---------- Tests -----------------------------------------------------------

def test_project_directory_exists_and_mode():
    assert os.path.isdir(PROJECT_DIR), (
        f"Required directory {PROJECT_DIR} is missing or not a directory."
    )
    _assert_path_mode(PROJECT_DIR, 0o700)


def test_artifacts_directory_exists_and_mode():
    assert os.path.isdir(ARTIFACTS_DIR), (
        f"Required directory {ARTIFACTS_DIR} is missing or not a directory."
    )
    _assert_path_mode(ARTIFACTS_DIR, 0o700)


def test_reports_directory_absent_initially():
    assert not os.path.exists(REPORTS_DIR), (
        f"{REPORTS_DIR} should NOT exist before the student runs their script."
    )


def test_list_txt_exists_regular_file_and_mode():
    assert os.path.isfile(LIST_TXT), (
        f"Seed data file {LIST_TXT} is missing or not a regular file."
    )
    _assert_path_mode(LIST_TXT, 0o644)


def test_list_txt_content_exact():
    with open(LIST_TXT, "r", encoding="utf-8", newline="") as fh:
        lines = fh.readlines()

    assert lines == EXPECTED_LIST_LINES, (
        "The content of list.txt does not match the expected seed data.\n"
        f"Expected {len(EXPECTED_LIST_LINES)} lines but found {len(lines)}.\n"
        "If the file was modified, restore it to the original state before "
        "running the task."
    )

    # Additional safety: ensure every line ends with LF and no extra blank lines
    for idx, line in enumerate(lines, start=1):
        assert line.endswith("\n"), (
            f"Line {idx} in list.txt does not end with a Unix LF newline."
        )