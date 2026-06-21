# test_initial_state.py
#
# Pytest suite that validates the *initial* on-disk layout **before** the
# student performs any action.  The tests confirm the presence of the expected
# raw-report CSVs and the absence of yet-to-be-created artefacts such as the
# `current_reports` directory or the audit log.

import os
from pathlib import Path

# ---------- CONSTANTS ----------
HOME = Path("/home/user")
FINOPS = HOME / "finops"
RAW = FINOPS / "raw_reports"
YEAR_2023 = RAW / "year=2023"
YEAR_2024 = RAW / "year=2024"

EXPECTED_DIRS = [
    FINOPS,
    RAW,
    YEAR_2023,
    YEAR_2024,
]

EXPECTED_FILES = [
    YEAR_2023 / "cost_report_2023-11.csv",
    YEAR_2023 / "cost_report_2023-12.csv",
    YEAR_2024 / "cost_report_2024-01.csv",
    YEAR_2024 / "cost_report_2024-02.csv",
    YEAR_2024 / "cost_report_2024-03.csv",
]

MUST_NOT_EXIST = [
    FINOPS / "current_reports",
    FINOPS / "symlink_creation.log",
]

# ---------- TESTS ----------


def _format_missing_paths(paths):
    """Helper for pretty-printing missing paths."""
    return "\n".join(f"  - {p}" for p in paths)


def test_required_directories_exist():
    """All mandatory directories must already be present on disk."""
    missing = [p for p in EXPECTED_DIRS if not p.is_dir()]
    assert not missing, (
        "The following required directories are missing or not directories:\n"
        f"{_format_missing_paths(missing)}"
    )


def test_expected_csv_files_exist():
    """Each month-level CSV must be present inside the raw_reports tree."""
    missing = [p for p in EXPECTED_FILES if not p.is_file()]
    assert not missing, (
        "The following expected CSV files are missing:\n"
        f"{_format_missing_paths(missing)}"
    )

    # Ensure none of the CSVs are symlinks (they must be real files).
    symlinks = [p for p in EXPECTED_FILES if p.is_symlink()]
    assert not symlinks, (
        "The following CSV paths are symbolic links but should be real files:\n"
        f"{_format_missing_paths(symlinks)}"
    )


def test_current_reports_directory_absent():
    """The `current_reports` directory should NOT exist yet."""
    current_reports = FINOPS / "current_reports"
    assert not current_reports.exists(), (
        f"Precondition failure: {current_reports} already exists, but the task "
        "requires creating it."
    )


def test_symlink_log_absent():
    """The symlink audit log should not exist before the task is executed."""
    log_path = FINOPS / "symlink_creation.log"
    assert not log_path.exists(), (
        f"Precondition failure: {log_path} already exists, but the task "
        "requires the student to create it."
    )