# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the workspace, i.e.
# before the student starts working on the task.  It checks that:
#   1. The two source CSV files exist at their absolute paths, have
#      precise, expected contents, and are world-readable (mode 0644).
#   2. No deliverable file or directory from the future task result
#      already exists.  The student must create them later.
#
# If any test fails the error message pinpoints exactly what is wrong.
#
# The suite relies only on the Python standard library + pytest.

import difflib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
OUTPUT_DIR = HOME / "output"

EMPLOYEE_MASTER = DATA_DIR / "employee_master.csv"
PAYROLL_Q1 = DATA_DIR / "payroll_Q1.csv"

EMPLOYEE_PAYROLL_TSV = OUTPUT_DIR / "employee_payroll_Q1.tsv"
PROCESS_LOG = OUTPUT_DIR / "process.log"

EXPECTED_EMPLOYEE_MASTER = (
    "EmployeeID,FullName,Department,Role,JoinDate\n"
    "1001,Ann Dowling,Engineering,DevOps,2015-06-11\n"
    "1002,Bob Tran,Sales,Account Manager,2018-03-17\n"
    "1003,Carla Méndez,HR,Recruiter,2019-11-05\n"
    "1004,Deepak Singh,Engineering,Backend Developer,2021-01-23\n"
    "1005,Eva Rossi,Finance,Accountant,2017-07-30\n"
)

EXPECTED_PAYROLL_Q1 = (
    "EmployeeID,Jan,Feb,Mar\n"
    "1001,12750,12900,12800\n"
    "1002,9450,9100,9300\n"
    "1003,8750,8800,8900\n"
    "1004,10600,10750,10850\n"
    "1006,9900,10050,10100\n"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _assert_mode_0644(path: Path):
    mode = path.stat().st_mode & 0o777
    assert mode == 0o644, (
        f"{path} exists but has mode {oct(mode)}; expected 0o644 (rw-r--r--)"
    )


def _compare_file_contents(actual: str, expected: str, path: Path):
    if actual != expected:
        diff = "\n".join(difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="expected",
            tofile=str(path),
            lineterm=""
        ))
        pytest.fail(
            f"Contents of {path} do not match the expected initial data:\n{diff}"
        )


# ---------------------------------------------------------------------------
# Tests for the data directory and source CSV files
# ---------------------------------------------------------------------------

def test_data_directory_present():
    assert DATA_DIR.is_dir(), f"Required directory {DATA_DIR} is missing."


@pytest.mark.parametrize("path,expected_contents", [
    (EMPLOYEE_MASTER, EXPECTED_EMPLOYEE_MASTER),
    (PAYROLL_Q1, EXPECTED_PAYROLL_Q1),
])
def test_source_files_exist_and_match(path: Path, expected_contents: str):
    assert path.is_file(), f"Required file {path} is missing."
    _assert_mode_0644(path)
    actual = path.read_text(encoding="utf-8")
    _compare_file_contents(actual, expected_contents, path)


# ---------------------------------------------------------------------------
# Tests ensuring the result artefacts do *not* exist yet
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path_description,path_obj", [
    ("output directory", OUTPUT_DIR),
    ("report TSV", EMPLOYEE_PAYROLL_TSV),
    ("process log", PROCESS_LOG),
])
def test_no_deliverables_yet(path_description: str, path_obj: Path):
    assert not path_obj.exists(), (
        f"{path_description.capitalize()} {path_obj} already exists, "
        "but the student has not produced any deliverables yet.  "
        "Please remove it so the task starts from a clean state."
    )