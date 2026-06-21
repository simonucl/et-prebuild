# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the filesystem
# before the student performs any actions.  It ensures that the three
# dashboard JSON files are present with the expected TEMP-prefixed UIDs,
# that no file has yet been modified, and that no log file exists.

import json
import os
from pathlib import Path

import pytest

DASHBOARD_DIR = Path("/home/user/dashboards/new")
EXPECTED_FILES = {
    "system_overview.json": "TEMP-abc123",
    "db_metrics.json":      "TEMP-db789",
    "queue_depth.json":     "TEMP-queue456",
}
LOG_FILE = Path("/home/user/dashboard_fix.log")


def _read_json(path: Path) -> dict:
    """
    Read a single-line JSON file using UTF-8.
    The helper raises a clear assertion error if the file is not valid JSON.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        pytest.fail(f"Required file missing: {path}", pytrace=False)

    # Ensure the file is a single line to match the spec.
    assert raw.count("\n") == 0, (
        f"{path} should be a single-line JSON document but contains newlines."
    )

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{path} is not valid JSON: {exc}", pytrace=False)


def test_dashboard_directory_exists():
    assert DASHBOARD_DIR.is_dir(), f"Directory {DASHBOARD_DIR} does not exist."


def test_expected_json_files_present_and_no_extra_json_files():
    # Check that the expected files exist
    for fname in EXPECTED_FILES:
        fpath = DASHBOARD_DIR / fname
        assert fpath.is_file(), f"Expected dashboard file missing: {fpath}"

    # Ensure there are no additional *.json files in the directory
    json_files_on_disk = {p.name for p in DASHBOARD_DIR.glob("*.json")}
    assert json_files_on_disk == set(EXPECTED_FILES.keys()), (
        "Directory {0} should contain exactly three JSON files: {1}. "
        "Found: {2}".format(
            DASHBOARD_DIR,
            ", ".join(EXPECTED_FILES),
            ", ".join(sorted(json_files_on_disk)) or "none",
        )
    )


@pytest.mark.parametrize("filename,expected_uid", EXPECTED_FILES.items())
def test_each_json_has_temp_prefixed_uid(filename, expected_uid):
    fpath = DASHBOARD_DIR / filename
    doc = _read_json(fpath)

    assert "uid" in doc, f'"uid" key missing in {fpath}.'
    actual_uid = doc["uid"]
    assert actual_uid == expected_uid, (
        f"{fpath} has unexpected UID.\n"
        f"Expected: {expected_uid}\n"
        f"Found:    {actual_uid}"
    )
    assert actual_uid.startswith("TEMP-"), (
        f'{fpath}: UID should start with "TEMP-" in the initial state.'
    )
    assert not actual_uid.startswith("PERM-"), (
        f'{fpath}: UID already starts with "PERM-"; '
        "it should still be TEMP-prefixed before the task is run."
    )


def test_log_file_not_present_yet():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should not exist before the student runs their solution."
    )