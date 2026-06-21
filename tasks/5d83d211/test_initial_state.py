# test_initial_state.py
#
# Pytest suite that validates the repository *before* the student
# performs any action.  These tests intentionally expect the original,
# un-modified files to be present so that the grader can be confident
# the exercise starts from a known state.
#
# The required initial state is:
#   • /home/user/project/.github/workflows/ci.yml      -> node-version must be 16
#   • /home/user/project/pyproject.toml                -> version must be 0.1.0
#   • /home/user/project/update_report.log             -> must NOT exist yet
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import pytest


PROJECT_ROOT = Path("/home/user/project")
CI_FILE = PROJECT_ROOT / ".github" / "workflows" / "ci.yml"
TOML_FILE = PROJECT_ROOT / "pyproject.toml"
REPORT_FILE = PROJECT_ROOT / "update_report.log"


@pytest.fixture(scope="module")
def ci_file_contents():
    """Return the raw lines of the ci.yml file."""
    if not CI_FILE.exists():
        pytest.fail(f"Expected {CI_FILE} to exist, but it is missing.")
    return CI_FILE.read_text(encoding="utf-8").splitlines()


@pytest.fixture(scope="module")
def toml_file_contents():
    """Return the raw lines of the pyproject.toml file."""
    if not TOML_FILE.exists():
        pytest.fail(f"Expected {TOML_FILE} to exist, but it is missing.")
    return TOML_FILE.read_text(encoding="utf-8").splitlines()


def _extract_node_version(lines):
    """
    Extract the value of `node-version:` from the provided list of lines.
    Returns the value as a string, with any surrounding quotes removed.
    """
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("node-version:"):
            # Split on *first* colon only to allow comments later in the line.
            value_part = stripped.split(":", 1)[1]
            # Remove comments after a space + '#' (YAML comment)
            value_part = value_part.split("#", 1)[0]
            value_part = value_part.strip()
            # Strip surrounding quotes if present
            if (value_part.startswith(("'", '"')) and
                    value_part.endswith(("'", '"')) and
                    len(value_part) >= 2):
                value_part = value_part[1:-1]
            return value_part
    return None


def _extract_poetry_version(lines):
    """
    Extract the version declared under the [tool.poetry] table.
    The search stops at the first blank line or another table header.
    """
    in_poetry_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_poetry_table = stripped == "[tool.poetry]"
            continue
        if in_poetry_table and stripped.startswith("version"):
            _, value_part = stripped.split("=", 1)
            value_part = value_part.strip()
            # Remove surrounding quotes
            if value_part.startswith(("'", '"')) and value_part.endswith(("'", '"')):
                value_part = value_part[1:-1]
            return value_part
    return None


def test_ci_yaml_has_node_version_16(ci_file_contents):
    """The GitHub Actions workflow must still target Node 16 initially."""
    node_version = _extract_node_version(ci_file_contents)
    assert node_version is not None, (
        f"'node-version:' key not found in {CI_FILE}. "
        "The initial workflow file appears to be malformed."
    )
    assert node_version == "16", (
        f"Expected node-version 16 in {CI_FILE}, "
        f"but found '{node_version}'. "
        "The initial state looks altered: it should use Node 16."
    )


def test_pyproject_toml_has_version_0_1_0(toml_file_contents):
    """The pyproject.toml must still advertise version 0.1.0 initially."""
    poetry_version = _extract_poetry_version(toml_file_contents)
    assert poetry_version is not None, (
        f"'version' key inside [tool.poetry] not found in {TOML_FILE}. "
        "The file might be damaged."
    )
    assert poetry_version == "0.1.0", (
        f"Expected version 0.1.0 in {TOML_FILE}, "
        f"but found '{poetry_version}'. "
        "The initial state should start at version 0.1.0."
    )


def test_update_report_log_not_present_yet():
    """No update_report.log should exist before the student runs their command."""
    assert not REPORT_FILE.exists(), (
        f"{REPORT_FILE} already exists. "
        "It should only be created after the student performs the required edits."
    )