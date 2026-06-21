# test_initial_state.py
#
# This pytest suite verifies that the repository is still in its *original*
# state before the student makes any modifications.  In particular, it checks
# that:
#   1. The GitHub workflow file contains only the initial “branches” list
#      (with the single bracket-style syntax) and no “env” block.
#   2. The TOML configuration file still exposes port 8080.
#   3. The update_log.txt file has not yet been created.
#
# Any deviation from these expectations produces a clear, actionable failure
# message.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
WORKFLOW_FILE = PROJECT_DIR / ".github" / "workflows" / "build.yml"
TOML_FILE = PROJECT_DIR / "config.toml"
UPDATE_LOG_FILE = HOME / "update_log.txt"


@pytest.fixture(scope="module")
def workflow_content():
    """Return the *raw* text of the current build.yml file."""
    if not WORKFLOW_FILE.exists():
        pytest.fail(f"Expected workflow file missing: {WORKFLOW_FILE}")
    return WORKFLOW_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def toml_content():
    """Return the *raw* text of the current config.toml file."""
    if not TOML_FILE.exists():
        pytest.fail(f"Expected TOML file missing: {TOML_FILE}")
    return TOML_FILE.read_text(encoding="utf-8")


def test_workflow_file_matches_initial_state(workflow_content):
    """
    The workflow YAML should still contain:
      * A single-line branch filter with `[ "main" ]`
      * No individual `- main` / `- develop` list items
      * No `env:` block
    """
    expected = (
        "name: Build Pipeline\n"
        "on:\n"
        "  push:\n"
        '    branches: [ "main" ]\n'
        "jobs:\n"
        "  build:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v2\n"
        "      - name: Run build\n"
        '        run: echo "Building..."\n'
    )

    # Allow a trailing newline at the end of the file, but content must match.
    actual = workflow_content
    if actual.endswith("\n") and not expected.endswith("\n"):
        expected += "\n"

    assert actual == expected, (
        f"The workflow file has changed from the initial state.\n\n"
        f"--- Expected content ---\n{expected}\n"
        f"--- Actual content   ---\n{actual}\n"
        "Differences indicate that the student modified the file too early."
    )

    # Additional sanity checks to catch subtle mistakes
    assert "- develop" not in actual, (
        "The workflow file already contains '- develop', "
        "but it should only have the bracketed list '[ \"main\" ]' at this stage."
    )
    assert "env:" not in actual, (
        "The workflow file already contains an 'env:' block, "
        "but it should not exist before the student performs the task."
    )


def test_toml_file_matches_initial_state(toml_content):
    """
    The config.toml file should still expose port 8080 exactly, with no blank
    lines before or after.
    """
    expected = "[server]\nport = 8080\n"

    actual = toml_content
    if actual.endswith("\n") and not expected.endswith("\n"):
        expected += "\n"

    assert actual == expected, (
        f"The TOML configuration file has been altered.\n\n"
        f"--- Expected content ---\n{expected}\n"
        f"--- Actual content   ---\n{actual}\n"
        "The server port must remain 8080 until the student updates it."
    )


def test_update_log_absent():
    """The update_log.txt file must not exist before the student creates it."""
    assert not UPDATE_LOG_FILE.exists(), (
        f"Found unexpected file: {UPDATE_LOG_FILE}\n"
        "The update log should only be created after the configuration changes "
        "have been applied."
    )