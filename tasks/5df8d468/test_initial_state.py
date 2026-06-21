# test_initial_state.py
#
# This pytest suite verifies the **initial** workstation state
# prior to the student’s remediation work.  It checks that:
#
# 1. The optimisation–solver directory exists.
# 2. The expected *.version files (and only those) are present.
# 3. Each *.version file contains exactly one line with the
#    correct version string and a single trailing newline (LF).
# 4. The compliance directory and report file do **not** yet exist.
#
# Any failure message will clearly indicate what is missing
# or unexpected in the environment.

import os
from pathlib import Path

import pytest

# Constants
HOME = Path("/home/user")
SOLVER_DIR = HOME / "opt_solvers"
COMPLIANCE_DIR = HOME / "compliance"
REPORT_FILE = COMPLIANCE_DIR / "solver_audit.log"

EXPECTED_SOLVERS = {
    "cbc": "2.10.7\n",
    "glpk": "5.0\n",
    "ortools": "9.6\n",
}


def test_solver_directory_exists_and_is_directory():
    assert SOLVER_DIR.exists(), f"Required directory {SOLVER_DIR} does not exist."
    assert SOLVER_DIR.is_dir(), f"{SOLVER_DIR} exists but is not a directory."


def test_expected_version_files_present_and_no_extras():
    # Collect *.version files actually present
    actual_version_files = {p.name for p in SOLVER_DIR.glob("*.version")}
    expected_version_files = {f"{name}.version" for name in EXPECTED_SOLVERS}

    # Missing files
    missing = expected_version_files - actual_version_files
    assert not missing, (
        "The following *.version files are missing from "
        f"{SOLVER_DIR}: {', '.join(sorted(missing))}"
    )

    # Unexpected extra files
    extras = actual_version_files - expected_version_files
    assert not extras, (
        "Unexpected *.version files present in "
        f"{SOLVER_DIR}: {', '.join(sorted(extras))}"
    )


@pytest.mark.parametrize("solver,expected_content", EXPECTED_SOLVERS.items())
def test_each_version_file_has_correct_single_line_content(solver, expected_content):
    version_file = SOLVER_DIR / f"{solver}.version"

    # Sanity: file must exist and be a file
    assert version_file.exists(), f"Expected file {version_file} does not exist."
    assert version_file.is_file(), f"{version_file} exists but is not a regular file."

    # Read and validate content
    with version_file.open("r", encoding="utf-8") as fh:
        content = fh.read()

    # Ensure the entire file content matches exactly (including trailing LF)
    assert content == expected_content, (
        f"Version file {version_file} has unexpected content.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Actual:   {repr(content)}"
    )

    # Additional guard: ensure there is exactly one line
    lines = content.splitlines(keepends=False)
    assert len(lines) == 1, (
        f"Version file {version_file} should contain exactly one line; "
        f"found {len(lines)} lines."
    )


def test_compliance_directory_and_report_do_not_exist_yet():
    assert not COMPLIANCE_DIR.exists(), (
        f"{COMPLIANCE_DIR} should not exist before the task is performed."
    )
    assert not REPORT_FILE.exists(), (
        f"{REPORT_FILE} should not exist before the task is performed."
    )