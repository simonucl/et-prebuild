# test_initial_state.py
#
# This test-suite verifies that the machine starts in the **expected initial
# state** *before* the student performs any work.  It checks for
# - presence of the schema and raw-report files
# - absence of any artefacts that the student has to create
# - basic sanity of the raw JSON documents
#
# All paths are absolute as required.

import json
import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
BASE_DIR = HOME / "storage_audit"
SCHEMA_FILE = BASE_DIR / "schema" / "disk_report.schema.json"
RAW_DIR = BASE_DIR / "raw_reports"
RAW_FILES = [
    RAW_DIR / "daily_storage01.json",
    RAW_DIR / "daily_storage02.json",
    RAW_DIR / "daily_storage03.json",
]
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "validation.log"
SUMMARY_DIR = BASE_DIR / "summary"
SUMMARY_FILE = SUMMARY_DIR / "disk_usage_summary.json"


def _is_readable(path: Path) -> bool:
    """Return True if `path` is readable by the current user."""
    return os.access(path, os.R_OK)


def test_base_directory_structure():
    assert BASE_DIR.is_dir(), f"Expected directory {BASE_DIR} to exist."

    # Schema directory and file
    schema_dir = SCHEMA_FILE.parent
    assert schema_dir.is_dir(), f"Expected directory {schema_dir} to exist."
    assert SCHEMA_FILE.is_file(), f"Schema file {SCHEMA_FILE} is missing."
    assert _is_readable(SCHEMA_FILE), f"Schema file {SCHEMA_FILE} is not readable."

    # Raw reports directory
    assert RAW_DIR.is_dir(), f"Expected directory {RAW_DIR} to exist."


@pytest.mark.parametrize("file_path", RAW_FILES)
def test_raw_report_files_present(file_path: Path):
    assert file_path.is_file(), f"Raw report {file_path} is missing."
    assert _is_readable(file_path), f"Raw report {file_path} is not readable."


def test_no_extra_raw_reports():
    """Ensure exactly the expected three JSON files are present in raw_reports/."""
    json_files = sorted(RAW_DIR.glob("*.json"))
    expected = sorted(RAW_FILES)
    assert json_files == expected, (
        "Unexpected set of JSON files in "
        f"{RAW_DIR}. Expected exactly {len(expected)} files:\n"
        + "\n".join(str(p) for p in expected)
    )


def test_raw_reports_are_valid_json():
    """All pre-seeded raw reports must parse as valid JSON."""
    for file_path in RAW_FILES:
        try:
            with file_path.open() as fp:
                json.load(fp)
        except json.JSONDecodeError as exc:
            pytest.fail(f"File {file_path} contains invalid JSON: {exc}")


def test_student_output_does_not_exist_yet():
    """
    Before the student runs their solution, no artefacts must be present:
    - logs/ directory may exist, but validation.log must **not**.
    - summary/ directory must not exist at all.
    """
    if LOG_DIR.exists():
        assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
        assert not LOG_FILE.exists(), (
            f"Output file {LOG_FILE} already exists. "
            "It should be created by the student's code."
        )
    else:
        # Directory itself is also expected to be absent initially.
        assert not LOG_DIR.exists(), f"{LOG_DIR} should not exist yet."

    assert not SUMMARY_DIR.exists(), (
        f"{SUMMARY_DIR} should not exist before the student's code runs."
    )
    assert not SUMMARY_FILE.exists(), (
        f"{SUMMARY_FILE} should not exist before the student's code runs."
    )


def test_permissions_of_existing_items():
    """
    Verify that existing files and directories have at least the minimal
    permissions expected for readability.
    """
    # Directories must be readable and executable (walkable)
    for directory in [BASE_DIR, SCHEMA_FILE.parent, RAW_DIR]:
        mode = directory.stat().st_mode
        assert mode & stat.S_IRUSR, f"Directory {directory} is not readable."
        assert mode & stat.S_IXUSR, f"Directory {directory} is not accessible (execute bit missing)."

    # Files must be readable
    for file_path in [SCHEMA_FILE, *RAW_FILES]:
        assert _is_readable(file_path), f"File {file_path} is not readable by the current user."