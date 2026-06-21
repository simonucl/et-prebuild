# test_initial_state.py
#
# Pytest suite that verifies the pristine filesystem/OS state
# before the student begins any work.  It **must** match the
# exercise description; otherwise the subsequent grading steps
# would be meaningless.
#
# IMPORTANT:  This file intentionally checks ONLY the inputs that
# are supposed to exist prior to the student’s actions.  It does
# *not* look for any of the output artefacts that the student is
# expected to create (such as /home/user/restore_validation.log
# or /home/user/restore_summary.json).

import json
import os
import stat
import sys
from pathlib import Path

import pytest

HOME = Path("/home/user")
MANIFEST_PATH = HOME / "backups" / "latest" / "manifest.json"
SCHEMA_PATH = HOME / "schema" / "restore-schema.json"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def _assert_is_regular_file(path: Path):
    assert path.exists(), f"Expected file {path} to exist, but it does not."
    assert path.is_file(), f"Expected {path} to be a regular file."
    # Extra safety: ensure it is not zero-length
    assert path.stat().st_size > 0, f"Expected {path} to be non-empty."


def _load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{path} contains invalid JSON: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_directory_structure():
    """
    Validate that the required directories exist.
    """
    backups_dir = HOME / "backups"
    latest_dir = backups_dir / "latest"
    schema_dir = HOME / "schema"

    assert backups_dir.is_dir(), f"Missing directory: {backups_dir}"
    assert latest_dir.is_dir(), f"Missing directory: {latest_dir}"
    assert schema_dir.is_dir(), f"Missing directory: {schema_dir}"


def test_manifest_file_presence_and_valid_json():
    """
    The manifest file must exist, be a regular file, and contain valid JSON.
    """
    _assert_is_regular_file(MANIFEST_PATH)

    manifest = _load_json(MANIFEST_PATH)

    # ---------------------------------------------------------------------
    # Rule 2.a – top-level backupId
    # ---------------------------------------------------------------------
    assert "backupId" in manifest, 'Key "backupId" missing from manifest.'
    assert (
        manifest["backupId"] == "BK2023-10-05"
    ), f'backupId is "{manifest["backupId"]}", expected "BK2023-10-05".'

    # ---------------------------------------------------------------------
    # Rule 2.b – restorePoints structure
    # ---------------------------------------------------------------------
    assert "restorePoints" in manifest, 'Key "restorePoints" missing from manifest.'
    restore_points = manifest["restorePoints"]
    assert isinstance(
        restore_points, list
    ), '"restorePoints" must be an array (list).'
    assert (
        len(restore_points) == 3
    ), f'Expected exactly 3 restore points, found {len(restore_points)}.'

    required_fields = {"id", "timestamp", "sizeBytes", "checksum"}
    for idx, rp in enumerate(restore_points, start=1):
        assert isinstance(
            rp, dict
        ), f"Restore point #{idx} should be an object, found {type(rp).__name__}."
        missing = required_fields - rp.keys()
        assert not missing, f"Restore point #{idx} missing keys: {', '.join(sorted(missing))}"
        for field in required_fields:
            assert rp[field] is not None, f"Restore point #{idx} field '{field}' is null."

        # Type checks
        assert isinstance(rp["id"], str), f"Restore point #{idx} 'id' must be a string."
        assert isinstance(
            rp["timestamp"], str
        ), f"Restore point #{idx} 'timestamp' must be a string."
        assert isinstance(
            rp["sizeBytes"], int
        ), f"Restore point #{idx} 'sizeBytes' must be an integer."
        assert (
            rp["sizeBytes"] >= 0
        ), f"Restore point #{idx} 'sizeBytes' must be non-negative."
        assert isinstance(
            rp["checksum"], str
        ), f"Restore point #{idx} 'checksum' must be a string."

    # ---------------------------------------------------------------------
    # Bonus sanity check – total size matches expectation
    # ---------------------------------------------------------------------
    total_size = sum(rp["sizeBytes"] for rp in restore_points)
    expected_total = 157_286_400  # 3 × 50 MiB
    assert (
        total_size == expected_total
    ), f"Total sizeBytes is {total_size}, expected {expected_total}."


def test_schema_file_presence_and_content():
    """
    Ensure the JSON schema file exists and references the same backupId constraint.
    """
    _assert_is_regular_file(SCHEMA_PATH)
    schema = _load_json(SCHEMA_PATH)

    # Basic structural sanity checks
    assert schema.get("type") == "object", "Schema 'type' must be 'object'."
    required_keys = schema.get("required", [])
    for key in ("backupId", "restorePoints"):
        assert (
            key in required_keys
        ), f'Schema "required" array must include "{key}".'

    # Validate that schema constrains backupId to the expected constant
    backup_id_const = (
        schema.get("properties", {})
        .get("backupId", {})
        .get("const")
    )
    assert (
        backup_id_const == "BK2023-10-05"
    ), f'Schema expects backupId "{backup_id_const}", should be "BK2023-10-05".'


def test_jq_is_available_in_path():
    """
    Although the instructions suggest using `jq`, it should already be
    installed and discoverable via the PATH.
    """
    from shutil import which

    jq_path = which("jq")
    assert jq_path, "The 'jq' command must be installed and in the PATH."


# ---------------------------------------------------------------------------
# End of file
# ---------------------------------------------------------------------------