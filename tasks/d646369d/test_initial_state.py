# test_initial_state.py
#
# This pytest suite verifies that the **initial** operating-system / filesystem
# state is correct *before* the student performs any action.  It checks only the
# pre-existing backup payloads and schema files; it deliberately avoids looking
# for output artefacts such as /home/user/restore_logs.

import json
from pathlib import Path

BACKUPS_DIR = Path("/home/user/backups")
SCHEMAS_DIR = Path("/home/user/schemas")

BACKUP_FILES = {
    "finance.json",
    "hr.json",
    "it.json",
}

SCHEMA_FILES = {
    "finance_schema.json",
    "hr_schema.json",
    "it_schema.json",
}

EXPECTED_REQUIRED_KEYS = ["id", "last_backup", "data"]


def test_backups_directory_exists():
    assert BACKUPS_DIR.is_dir(), (
        "Missing directory: '/home/user/backups' – the restored payloads should be "
        "located here."
    )


def test_schemas_directory_exists():
    assert SCHEMAS_DIR.is_dir(), (
        "Missing directory: '/home/user/schemas' – the JSON schema files should be "
        "located here."
    )


def test_expected_backup_files_present_and_only_them():
    present = {p.name for p in BACKUPS_DIR.glob("*.json")}
    missing = BACKUP_FILES - present
    extra = present - BACKUP_FILES
    assert not missing, (
        "The following expected JSON backup files are missing from "
        f"'{BACKUPS_DIR}': {', '.join(sorted(missing))}"
    )
    assert not extra, (
        "Unexpected extra JSON files present in "
        f"'{BACKUPS_DIR}': {', '.join(sorted(extra))}"
    )


def test_expected_schema_files_present_and_only_them():
    present = {p.name for p in SCHEMAS_DIR.glob("*.json")}
    missing = SCHEMA_FILES - present
    extra = present - SCHEMA_FILES
    assert not missing, (
        "The following expected JSON schema files are missing from "
        f"'{SCHEMAS_DIR}': {', '.join(sorted(missing))}"
    )
    assert not extra, (
        "Unexpected extra JSON schema files present in "
        f"'{SCHEMAS_DIR}': {', '.join(sorted(extra))}"
    )


def _load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"File '{path}' is not valid JSON: {exc}") from exc


def test_backup_json_structure():
    """
    Each backup file must be valid JSON and contain at least the keys
    specified by the schema's 'required' list (id, last_backup, data).
    """
    for filename in BACKUP_FILES:
        path = BACKUPS_DIR / filename
        data = _load_json(path)
        assert isinstance(data, dict), (
            f"Backup file '{path}' should contain a JSON object at the root."
        )
        for key in EXPECTED_REQUIRED_KEYS:
            assert key in data, (
                f"Backup file '{path}' is missing required key '{key}'."
            )


def test_schema_json_structure():
    """
    Each schema file must be valid JSON and contain exactly the 'required' array
    with the expected keys.
    """
    for filename in SCHEMA_FILES:
        path = SCHEMAS_DIR / filename
        schema = _load_json(path)

        assert isinstance(schema, dict), (
            f"Schema file '{path}' should contain a JSON object at the root."
        )
        assert "required" in schema, (
            f"Schema file '{path}' must define a top-level 'required' key."
        )
        required = schema["required"]
        assert isinstance(required, list), (
            f"The 'required' value in '{path}' must be a list."
        )
        assert sorted(required) == sorted(EXPECTED_REQUIRED_KEYS), (
            f"Schema file '{path}' has an unexpected 'required' list "
            f"(expected {EXPECTED_REQUIRED_KEYS}, got {required})."
        )