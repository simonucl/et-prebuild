# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem / OS state
# before the student performs any action on the CI prototype task.
# Only stdlib + pytest are used.

import os
import stat
from pathlib import Path

import pytest

CI_DIR = Path("/home/user/projects/ci")
PIPELINE_FILE = CI_DIR / "pipeline.yml"
CONFIG_DIR = CI_DIR / "config"
VARS_TOML = CONFIG_DIR / "vars.toml"
CHANGES_LOG = CI_DIR / "changes.log"

EXPECTED_PIPELINE_LINES = [
    'version: "1.0"\n',
    "jobs:\n",
    "  build:\n",
    "    steps:\n",
    "      - run: echo \"Building\"\n",
]

@pytest.fixture(scope="module")
def pipeline_content():
    """Return the contents of /home/user/projects/ci/pipeline.yml as a list of lines."""
    if not PIPELINE_FILE.exists():
        pytest.skip("pipeline.yml is missing; subsequent tests will fail meaningfully.")
    return PIPELINE_FILE.read_text(encoding="utf-8").splitlines(keepends=True)


def test_ci_directory_exists():
    assert CI_DIR.is_dir(), f"Expected directory {CI_DIR} to exist."


def test_pipeline_file_exists_and_is_readable():
    assert PIPELINE_FILE.is_file(), f"Expected file {PIPELINE_FILE} to exist."
    mode = PIPELINE_FILE.stat().st_mode
    assert mode & stat.S_IRUSR, f"{PIPELINE_FILE} should at least be owner-readable."


def test_pipeline_file_initial_content(pipeline_content):
    """Validate that pipeline.yml contains ONLY the build job—no test job yet."""
    # Basic sanity check: first five lines must match the expected template.
    assert pipeline_content[:5] == EXPECTED_PIPELINE_LINES, (
        f"{PIPELINE_FILE} does not contain the expected initial build job definition.\n"
        "It should look like:\n" + "".join(EXPECTED_PIPELINE_LINES)
    )

    # Ensure there is *no* test job present yet.
    unwanted_keywords = [" test:", "needs: [\"build\"]", "pytest -q"]
    for keyword in unwanted_keywords:
        assert all(keyword not in line for line in pipeline_content), (
            f"Found '{keyword.strip()}' in {PIPELINE_FILE}, but the initial state "
            "must NOT include the test job."
        )


def test_config_directory_absent():
    assert not CONFIG_DIR.exists(), (
        f"Directory {CONFIG_DIR} should NOT exist in the initial state."
    )


def test_vars_toml_absent():
    assert not VARS_TOML.exists(), (
        f"File {VARS_TOML} should NOT exist in the initial state."
    )


def test_changes_log_absent():
    assert not CHANGES_LOG.exists(), (
        f"File {CHANGES_LOG} should NOT exist in the initial state."
    )