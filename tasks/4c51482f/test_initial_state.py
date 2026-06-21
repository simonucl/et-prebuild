# test_initial_state.py
"""
Pytest suite that verifies the **initial** file system / OS state
*before* the student starts working on the task.

This file must remain untouched by the student – it is executed by the
automated grader to ensure the starting conditions are correct.

What is checked:

1. Required directories exist.
2. Required files exist.
3. The JSON manifest is syntactically valid **and** fulfils the essential
   constraints expressed in the supplied JSON-Schema — without using any
   external libraries (only Python stdlib is allowed here).

NOTE:
• We deliberately do **not** check for the presence of the output file
  `/home/user/dev/project_summary.txt`, because it is the artefact the
  student has to create.
"""

import json
import os
import re
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------#
# Constants
# ---------------------------------------------------------------------------#
HOME = Path("/home/user")
DEV_DIR = HOME / "dev"
CONFIG_DIR = DEV_DIR / "config"

MANIFEST_PATH = CONFIG_DIR / "project.json"
SCHEMA_PATH = CONFIG_DIR / "project.schema.json"

REQUIRED_DIRS = [DEV_DIR, CONFIG_DIR]
REQUIRED_FILES = [MANIFEST_PATH, SCHEMA_PATH]

# Regular expression the version string must satisfy: MAJOR.MINOR.PATCH
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


# ---------------------------------------------------------------------------#
# Helper functions
# ---------------------------------------------------------------------------#
def load_json(path: Path):
    """Load and return JSON from *path*; raise pytest failure on error."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        pytest.fail(f"Required file missing: {path}")
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}")


# ---------------------------------------------------------------------------#
# Tests
# ---------------------------------------------------------------------------#
@pytest.mark.parametrize("directory", REQUIRED_DIRS)
def test_required_directories_exist(directory: Path):
    assert directory.is_dir(), f"Required directory is missing: {directory}"


@pytest.mark.parametrize("file_path", REQUIRED_FILES)
def test_required_files_exist(file_path: Path):
    assert file_path.is_file(), f"Required file is missing: {file_path}"


def test_manifest_conforms_to_schema_semantics():
    """
    Perform a *light-weight* schema validation using stdlib only.

    The full JSON-Schema is stored in project.schema.json, but we cannot rely
    on the 'jsonschema' package.  Therefore we manually validate the essential
    constraints that matter for the downstream task.
    """
    # Sanity-check: the schema file is at least valid JSON
    _ = load_json(SCHEMA_PATH)

    manifest = load_json(MANIFEST_PATH)

    # ------------------------------------------------------------------ #
    # 1. Required top-level properties
    # ------------------------------------------------------------------ #
    required_keys = {"name", "version", "dependencies"}
    extra_keys = set(manifest) - required_keys
    missing_keys = required_keys - set(manifest)

    if missing_keys:
        pytest.fail(
            f"Manifest {MANIFEST_PATH} is missing required key(s): "
            f"{', '.join(sorted(missing_keys))}"
        )

    if extra_keys:
        pytest.fail(
            f"Manifest {MANIFEST_PATH} has unexpected key(s) not allowed by "
            f"the schema: {', '.join(sorted(extra_keys))}"
        )

    # ------------------------------------------------------------------ #
    # 2. Validate individual fields
    # ------------------------------------------------------------------ #
    # 2.1 name
    if not isinstance(manifest["name"], str):
        pytest.fail("Field 'name' must be a string")

    # 2.2 version (simple semver pattern: X.Y.Z where X,Y,Z are integers)
    version = manifest["version"]
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        pytest.fail(
            "Field 'version' must be a string matching the pattern "
            "'MAJOR.MINOR.PATCH' (e.g. 1.2.3)"
        )

    # 2.3 dependencies (object with string values)
    deps = manifest["dependencies"]
    if not isinstance(deps, dict):
        pytest.fail("Field 'dependencies' must be an object/mapping")

    bad_key_types = [k for k in deps if not isinstance(k, str)]
    bad_val_types = [k for k, v in deps.items() if not isinstance(v, str)]

    if bad_key_types:
        pytest.fail(
            f"Dependency names must be strings, but found non-string key(s): "
            f"{', '.join(map(str, bad_key_types))}"
        )

    if bad_val_types:
        pytest.fail(
            "Dependency versions must be strings, but the following "
            f"dependencies are not: {', '.join(bad_val_types)}"
        )

    # All good – manifest satisfies the essential schema constraints.
    assert True


def test_no_output_file_pre_existing():
    """
    Ensure the output artefact does NOT exist yet.
    This guarantees the student is responsible for creating it.
    """
    summary_path = DEV_DIR / "project_summary.txt"
    assert not summary_path.exists(), (
        f"Output file {summary_path} already exists. The student task "
        "should create this file; please remove it from the starter files."
    )