# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# BEFORE the student performs any actions required by the task.
#
# Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PIPELINE_DIR = Path("/home/user/projects/pipeline")
PIPELINE_YAML = PIPELINE_DIR / "pipeline.yaml"
CONFIG_TOML = PIPELINE_DIR / "config.toml"
UPDATE_LOG = PIPELINE_DIR / "update.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def file_contains(path: Path, substring: str) -> bool:
    """Return True if the substring is present anywhere in the file."""
    with path.open("r", encoding="utf-8") as fh:
        return substring in fh.read()


def file_lacks(path: Path, substring: str) -> bool:
    """Return True if the substring is NOT present anywhere in the file."""
    return not file_contains(path, substring)


def assert_readable_writable(path: Path):
    """Assert that the current user can read *and* write the given path."""
    st = path.stat()
    mode = stat.S_IMODE(st.st_mode)
    assert mode & stat.S_IRUSR, f"{path} is not readable by the current user"
    assert mode & stat.S_IWUSR, f"{path} is not writable by the current user"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directory_structure():
    """Required directory hierarchy must exist."""
    assert PIPELINE_DIR.exists(), f"Missing directory: {PIPELINE_DIR}"
    assert PIPELINE_DIR.is_dir(), f"{PIPELINE_DIR} exists but is not a directory"


def test_pipeline_yaml_exists_and_permissions():
    """pipeline.yaml must exist and be read/write accessible."""
    assert PIPELINE_YAML.exists(), f"Missing file: {PIPELINE_YAML}"
    assert PIPELINE_YAML.is_file(), f"{PIPELINE_YAML} exists but is not a file"
    assert_readable_writable(PIPELINE_YAML)


def test_pipeline_yaml_initial_content():
    """Validate the initial contents of pipeline.yaml."""
    content = PIPELINE_YAML.read_text(encoding="utf-8").splitlines()

    # 1. version must be 1
    assert any(line.strip() == "version: 1" for line in content), (
        "pipeline.yaml should have 'version: 1' as the top-level key before edits"
    )

    # 2. stages must contain only build and test (no integration yet)
    stages_lines = [l.strip() for l in content if l.strip().startswith("- ")]
    assert "- build" in stages_lines, "Stage 'build' missing from stages list"
    assert "- test" in stages_lines, "Stage 'test' missing from stages list"
    assert "- integration" not in stages_lines, (
        "Stage 'integration' should NOT be present in the initial file"
    )

    # 3. jobs section must include build_app and run_tests but NOT integration_test
    assert file_contains(PIPELINE_YAML, "build_app:"), "Job 'build_app' missing from pipeline.yaml"
    assert file_contains(PIPELINE_YAML, "run_tests:"), "Job 'run_tests' missing from pipeline.yaml"
    assert file_lacks(PIPELINE_YAML, "integration_test:"), (
        "Job 'integration_test' must NOT exist in the initial pipeline.yaml"
    )


def test_config_toml_exists_and_permissions():
    """config.toml must exist and be read/write accessible."""
    assert CONFIG_TOML.exists(), f"Missing file: {CONFIG_TOML}"
    assert CONFIG_TOML.is_file(), f"{CONFIG_TOML} exists but is not a file"
    assert_readable_writable(CONFIG_TOML)


def test_config_toml_initial_content():
    """Validate the initial contents of config.toml."""
    # 1. [build] table must NOT yet contain parallel_jobs
    assert file_lacks(CONFIG_TOML, "parallel_jobs"), (
        "'parallel_jobs' should NOT exist in the initial [build] table"
    )

    # 2. [release] should have version_code = 42 and track = "beta"
    assert file_contains(CONFIG_TOML, "version_code = 42"), (
        "Initial config.toml should have 'version_code = 42'"
    )
    assert file_contains(CONFIG_TOML, 'track        = "beta"') or file_contains(
        CONFIG_TOML, 'track = "beta"'
    ), "Initial config.toml should have track set to \"beta\""

    # 3. No [notifications] table yet
    assert file_lacks(CONFIG_TOML, "[notifications]"), (
        "[notifications] table must NOT exist in the initial config.toml"
    )


def test_update_log_absent():
    """update.log must NOT exist before the student creates it."""
    assert not UPDATE_LOG.exists(), f"{UPDATE_LOG} should not exist before the task is performed"