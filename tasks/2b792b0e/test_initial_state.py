# test_initial_state.py
#
# This test-suite asserts that the *initial* state of the training
# environment is exactly what the task description promises.
# It intentionally stays clear of anything the student is supposed
# to create (/home/user/restore , /home/user/validation, …).
#
# The tests only rely on the Python stdlib + pytest.

import os
import json
import tarfile
import shutil
import textwrap
import pytest

HOME = "/home/user"

ARCHIVES_DIR = os.path.join(HOME, "archives")
SCHEMAS_DIR = os.path.join(HOME, "schemas")

TARBALL_PATH = os.path.join(ARCHIVES_DIR, "daily_backup.tar.gz")
SCHEMA_PATH = os.path.join(SCHEMAS_DIR, "backup_manifest.schema.json")

EXPECTED_VALID_MANIFEST = {
    "backupId": "bku-20231015-01",
    "timestamp": "2023-10-15T02:15:30Z",
    "files": [
        {"filename": "etc/passwd", "checksum": "a54d88e06612d820bc3be72877c74f257b561b19"},
        {"filename": "etc/shadow", "checksum": "2c1743a391305fbf367df8e4f069f9f9a46b3be2"},
    ],
}

EXPECTED_INVALID_MANIFEST = {
    "backupId": "bku-20231015-02",
    "timestamp": "2023-10-15T02:16:00Z",
    "files": "should-be-array-but-is-string",
}

EXPECTED_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["backupId", "timestamp", "files"],
    "properties": {
        "backupId": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "files": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["filename", "checksum"],
                "properties": {
                    "filename": {"type": "string"},
                    "checksum": {"type": "string", "pattern": "^[a-f0-9]{40}$"},
                },
            },
        },
    },
}


@pytest.mark.parametrize(
    "path,kind",
    [
        (ARCHIVES_DIR, "directory"),
        (SCHEMAS_DIR, "directory"),
        (TARBALL_PATH, "file"),
        (SCHEMA_PATH, "file"),
    ],
)
def test_required_paths_exist(path, kind):
    """
    Ensure that the promised directories and files are in place.
    """
    assert os.path.exists(path), f"Expected {kind} at {path!s} is missing."
    if kind == "directory":
        assert os.path.isdir(path), f"Expected {path!s} to be a directory."
    else:
        assert os.path.isfile(path), f"Expected {path!s} to be a regular file."


def test_tarball_contains_expected_members_and_contents():
    """
    The tarball must exist, contain the two JSON manifests under daily/,
    and the JSON inside each member must match the specification.
    """
    with tarfile.open(TARBALL_PATH, "r:gz") as tf:
        members = tf.getnames()

        for member_name in ("daily/valid_manifest.json", "daily/invalid_manifest.json"):
            assert (
                member_name in members
            ), f"Tarball is missing required member {member_name!r}"

        # Validate content of valid_manifest.json
        valid_file = tf.extractfile("daily/valid_manifest.json")
        assert valid_file is not None, "Could not read valid_manifest.json from tarball."
        valid_json = json.load(valid_file)
        assert (
            valid_json == EXPECTED_VALID_MANIFEST
        ), textwrap.dedent(
            f"""
            Content mismatch for daily/valid_manifest.json inside tarball.
            Expected:
            {json.dumps(EXPECTED_VALID_MANIFEST, indent=2)}
            Found:
            {json.dumps(valid_json, indent=2)}
            """
        )

        # Validate content of invalid_manifest.json
        invalid_file = tf.extractfile("daily/invalid_manifest.json")
        assert (
            invalid_file is not None
        ), "Could not read invalid_manifest.json from tarball."
        invalid_json = json.load(invalid_file)
        assert (
            invalid_json == EXPECTED_INVALID_MANIFEST
        ), textwrap.dedent(
            f"""
            Content mismatch for daily/invalid_manifest.json inside tarball.
            Expected:
            {json.dumps(EXPECTED_INVALID_MANIFEST, indent=2)}
            Found:
            {json.dumps(invalid_json, indent=2)}
            """
        )


def test_schema_file_matches_expected_json():
    """
    The JSON schema file on disk must match the specification exactly.
    (Ordering of keys does not matter; structural equality is enforced.)
    """
    with open(SCHEMA_PATH, "r", encoding="utf-8") as fh:
        actual_schema = json.load(fh)

    assert (
        actual_schema == EXPECTED_SCHEMA
    ), textwrap.dedent(
        f"""
        Content mismatch for {SCHEMA_PATH}.
        Expected:
        {json.dumps(EXPECTED_SCHEMA, indent=2)}
        Found:
        {json.dumps(actual_schema, indent=2)}
        """
    )


def test_jq_binary_is_available_in_path():
    """
    The exercise instructions rely on `jq` being installed.
    Make sure it's discoverable via the user's PATH.
    """
    jq_path = shutil.which("jq")
    assert jq_path, "The `jq` executable is not found in PATH; it is required for validation."