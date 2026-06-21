# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem state expected by
# the assignment is present.  It purposefully checks only the input artefacts
# that have to exist *before* the student begins to work.  It deliberately
# does **not** look for any script, log or output directories / files that the
# student is supposed to create later on.
#
# If any of the following tests fail, the error message will make clear which
# prerequisite item is missing or malformed.

import json
import os
from pathlib import Path

import pytest

# ----- constants -------------------------------------------------------------

HOME = Path("/home/user")
QA_DIR = HOME / "qa"
SAMPLES_DIR = QA_DIR / "json_samples"

SCHEMA_FILE = QA_DIR / "user_schema.json"
SAMPLE_FILES = [
    SAMPLES_DIR / "user1.json",
    SAMPLES_DIR / "user2.json",
    SAMPLES_DIR / "user3.json",
]

# ----- helpers ---------------------------------------------------------------


def _read_json(path: Path):
    """Read *path* and return decoded JSON.

    A helpful assertion message is produced on failure.
    """
    try:
        with path.open("rt", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"{path} contains invalid JSON: {exc}")  # noqa: PT013


# ----- tests -----------------------------------------------------------------


def test_required_directories_exist():
    """The mandatory directory structure must already be in place."""
    for directory in (QA_DIR, SAMPLES_DIR):
        assert directory.is_dir(), f"Missing directory: {directory}"


@pytest.mark.parametrize("file_path", [SCHEMA_FILE, *SAMPLE_FILES])
def test_required_files_exist(file_path: Path):
    """All fixture JSON files must exist as regular files."""
    assert file_path.is_file(), f"Missing file: {file_path}"


@pytest.mark.parametrize("file_path", [SCHEMA_FILE, *SAMPLE_FILES])
def test_files_contain_valid_json(file_path: Path):
    """Each fixture file must contain syntactically valid JSON."""
    _read_json(file_path)  # Parsing is performed inside helper; failures assert.


def test_schema_basic_structure():
    """The provided JSON-Schema should declare an object with required keys."""
    schema = _read_json(SCHEMA_FILE)

    # Basic, minimal sanity checks so downstream validation makes sense.
    assert schema.get("type") == "object", (
        f"{SCHEMA_FILE} should define an object schema, "
        f"but `.type` is {schema.get('type')!r}"
    )
    required_keys = {"id", "name", "email", "roles"}
    assert required_keys.issubset(set(schema.get("required", []))), (
        f"{SCHEMA_FILE} is expected to require the keys "
        f"{', '.join(sorted(required_keys))}"
    )


@pytest.mark.parametrize("file_path", SAMPLE_FILES)
def test_sample_files_have_mandatory_fields(file_path: Path):
    """Sample JSON objects must expose the keys referenced by the schema."""
    obj = _read_json(file_path)
    for key in ("id", "name", "email", "roles"):
        assert key in obj, f"{file_path} is missing the key '{key}'"


# -----------------------------------------------------------------------------
# Nothing beyond this point is checked because it belongs to the *output* arte-
# facts the student is tasked to generate.
# -----------------------------------------------------------------------------