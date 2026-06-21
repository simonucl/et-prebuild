# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state **before**
# the student performs any actions.  Do NOT modify these tests; make the
# system satisfy them by preparing the required initial files **only**.

import os
from pathlib import Path

SOURCE_DIR = Path("/home/user/source_configs")
BACKUP_DIR = Path("/home/user/backups")

EXPECTED_FILES = {
    "config1.yaml": "---\nservice: web\nreplicas: 3\n",
    "config2.ini": "[database]\nhost = db.internal\nport = 5432\n",
    "app.env": "APP_ENV=production\nDEBUG=false\n",
}


def test_source_directory_exists_and_is_dir():
    assert SOURCE_DIR.exists(), f"Required directory {SOURCE_DIR} is missing."
    assert SOURCE_DIR.is_dir(), f"{SOURCE_DIR} exists but is not a directory."


def test_backup_directory_does_not_exist_yet():
    assert not BACKUP_DIR.exists(), (
        f"{BACKUP_DIR} should NOT exist before the backup is created; "
        "please start with a clean state."
    )


def test_source_directory_contains_exact_files():
    entries = sorted(p.name for p in SOURCE_DIR.iterdir() if p.is_file())
    expected_entries = sorted(EXPECTED_FILES.keys())
    assert (
        entries == expected_entries
    ), f"{SOURCE_DIR} must contain exactly the files {expected_entries}. Found: {entries}"


def test_each_expected_file_has_correct_content():
    for filename, expected_content in EXPECTED_FILES.items():
        path = SOURCE_DIR / filename
        assert path.exists(), f"Expected file {path} is missing."
        assert path.is_file(), f"{path} exists but is not a regular file."
        with path.open("r", encoding="utf-8") as fh:
            data = fh.read()
        assert (
            data == expected_content
        ), f"Content of {path} does not match expected content.\nExpected:\n{expected_content!r}\nGot:\n{data!r}"