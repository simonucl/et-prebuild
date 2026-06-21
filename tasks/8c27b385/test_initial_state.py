# test_initial_state.py
#
# Pytest suite that validates the PRE-EXISTING operating-system / filesystem
# state before the student performs any action.

import hashlib
import json
import os
from pathlib import Path

# ----------  CONSTANTS ----------
HOME = Path("/home/user")
BACKUPS_DIR = HOME / "data" / "backups"
VALIDATION_DIR = HOME / "data" / "validation"

CSV_FILE = BACKUPS_DIR / "archive_2023-09-30.csv"
CSV_META_FILE = BACKUPS_DIR / "archive_2023-09-30.json"
NOTES_FILE = BACKUPS_DIR / "notes.txt"
MANIFEST_FILE = BACKUPS_DIR / "manifest.json"

EXPECTED_CSV_CONTENT = (
    "id,name,value\n"
    "1,alpha,100\n"
    "2,beta,200\n"
    "3,gamma,300\n"
)
EXPECTED_META_JSON = {
    "header": ["id", "name", "value"],
    "rows": 3,
}

# ----------  HELPERS ----------
def sha256_hex(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------  TESTS ----------
def test_backups_directory_exists_and_is_directory():
    assert BACKUPS_DIR.exists(), f"Directory {BACKUPS_DIR} is missing."
    assert BACKUPS_DIR.is_dir(), f"{BACKUPS_DIR} exists but is not a directory."


def test_required_files_exist():
    for file_path in (CSV_FILE, CSV_META_FILE, NOTES_FILE, MANIFEST_FILE):
        assert file_path.exists(), f"Required file {file_path} is missing."
        assert file_path.is_file(), f"{file_path} exists but is not a regular file."


def test_csv_content_exact_match():
    content = CSV_FILE.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_CSV_CONTENT
    ), f"{CSV_FILE} content does not match expected exactly.\nExpected:\n{EXPECTED_CSV_CONTENT!r}\nGot:\n{content!r}"


def test_csv_metadata_json_matches():
    meta = json.loads(CSV_META_FILE.read_text(encoding="utf-8"))
    assert (
        meta == EXPECTED_META_JSON
    ), f"{CSV_META_FILE} JSON content mismatch.\nExpected: {EXPECTED_META_JSON}\nGot:      {meta}"


def test_manifest_structure_and_hashes_are_correct():
    raw = MANIFEST_FILE.read_text(encoding="utf-8")
    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as e:
        raise AssertionError(f"{MANIFEST_FILE} is not valid JSON: {e}")

    assert isinstance(manifest, list), f"{MANIFEST_FILE} root element must be a JSON array."

    expected_files_order = ["archive_2023-09-30.csv", "notes.txt"]
    assert (
        [entry.get("file") for entry in manifest] == expected_files_order
    ), f"{MANIFEST_FILE} array must list files {expected_files_order} in that order."

    # Validate every entry
    for entry in manifest:
        # Required keys ONLY: 'file', 'sha256'
        assert set(entry.keys()) == {"file", "sha256"}, (
            f"Entry {entry} must contain ONLY keys 'file' and 'sha256' at initial state."
        )

        file_rel_path = entry["file"]
        sha_from_manifest = entry["sha256"]

        # Path must resolve correctly
        file_path = BACKUPS_DIR / file_rel_path
        assert file_path.exists(), f"Manifest references missing file {file_path}."

        # Ensure sha256_from_manifest is 64-char hex string
        assert (
            isinstance(sha_from_manifest, str)
            and len(sha_from_manifest) == 64
            and all(c in "0123456789abcdef" for c in sha_from_manifest.lower())
        ), (
            f"SHA-256 field for {file_rel_path} must be a 64-character hex string."
        )

        actual_sha = sha256_hex(file_path)
        assert (
            actual_sha == sha_from_manifest
        ), f"SHA-256 mismatch for {file_rel_path}: manifest has {sha_from_manifest}, actual is {actual_sha}."


def test_notes_content_matches():
    expected_notes = "Backup created on 2023-09-30 at 03:00 UTC.\n"
    notes_content = NOTES_FILE.read_text(encoding="utf-8")
    assert (
        notes_content == expected_notes
    ), f"{NOTES_FILE} content mismatch.\nExpected: {expected_notes!r}\nGot:      {notes_content!r}"


def test_validation_directory_does_not_exist_yet():
    assert not VALIDATION_DIR.exists(), (
        f"Directory {VALIDATION_DIR} should NOT exist before the student runs their solution."
    )