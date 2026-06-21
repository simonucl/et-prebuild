# test_initial_state.py
# Pytest suite that validates the starting filesystem state for the
# “FinOps Q2-2023 report patch” exercise.
#
# These tests assert that the workspace is exactly as described *before*
# the student performs any action.  If any assertion fails, the error
# message pinpoints what is missing or incorrect so the learner can fix
# the setup before proceeding.
#
# Allowed imports: only stdlib + pytest.

import os
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Paths that must already exist
# ---------------------------------------------------------------------------
HOME = Path("/home/user")
REPORT_DIR = HOME / "finops_reports"
CSV_PATH = REPORT_DIR / "cost_report_Q2_2023.csv"
PATCH_PATH = REPORT_DIR / "cost_report_Q2_2023.patch"


# ---------------------------------------------------------------------------
# Expected file contents as provided in the task description
# (Every line below — including the very last one — *must* end with '\n')
# ---------------------------------------------------------------------------
EXPECTED_CSV_CONTENT = (
    "Project,Service,Month,CostUSD\n"
    "ProjectA,Compute,2023-04,1500.00\n"
    "ProjectA,Storage,2023-04,200.00\n"
    "ProjectB,Compute,2023-04,1800.00\n"
    "ProjectB,Database,2023-04,600.00\n"
)

EXPECTED_PATCH_CONTENT = (
    "--- cost_report_Q2_2023.csv\t2023-05-01 12:00:00.000000000 +0000\n"
    "+++ cost_report_Q2_2023.csv\t2023-05-02 12:00:00.000000000 +0000\n"
    "@@ -1,5 +1,6 @@\n"
    " Project,Service,Month,CostUSD\n"
    " ProjectA,Compute,2023-04,1500.00\n"
    "-ProjectA,Storage,2023-04,200.00\n"
    "+ProjectA,Storage,2023-04,150.00\n"
    " ProjectB,Compute,2023-04,1800.00\n"
    "-ProjectB,Database,2023-04,600.00\n"
    "+ProjectB,Database,2023-04,450.00\n"
    "+ProjectC,Analytics,2023-04,300.00\n"
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def read_text(path: Path) -> str:
    """Read UTF-8 text from *path*; raise a clear error if the file is absent."""
    if not path.exists():
        pytest.fail(f"Required file is missing: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")  # noqa: TRY003


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_report_directory_exists():
    assert REPORT_DIR.is_dir(), (
        f"Directory {REPORT_DIR} should exist before starting the exercise."
    )


def test_required_files_exist():
    missing = [str(p) for p in (CSV_PATH, PATCH_PATH) if not p.exists()]
    assert not missing, f"The following required file(s) are missing: {', '.join(missing)}"


def test_csv_initial_contents_are_unchanged():
    """Validate that the CSV has *not* yet been patched."""
    actual = read_text(CSV_PATH)
    assert actual == EXPECTED_CSV_CONTENT, (
        f"{CSV_PATH} does not match the expected pre-patch contents.\n"
        "Ensure you start with the unmodified cost report supplied in the task description."
    )


def test_patch_file_contents_are_exact():
    """Ensure the .patch file is present and unaltered."""
    actual = read_text(PATCH_PATH)
    assert actual == EXPECTED_PATCH_CONTENT, (
        f"{PATCH_PATH} does not match the expected patch data.\n"
        "Do not modify the patch file before running the exercise."
    )