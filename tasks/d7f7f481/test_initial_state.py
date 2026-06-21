# test_initial_state.py
#
# This test-suite validates that the *initial* project filesystem state is
# exactly as expected *before* the student performs any actions.
#
# 1. /home/user/project must exist.
# 2. /home/user/project/app.yaml must exist and contain ONLY the original
#    YAML snippet (no “logging:” section yet).
# 3. /home/user/project/pyproject.toml must exist, still at version 0.1.0.
# 4. /home/user/project/README.md must exist (content is not checked).
#
# The tests are intentionally strict about content and ordering so that any
# pre-existing divergence is caught early and reported with a clear message.

import os
from pathlib import Path

import pytest

PROJECT_DIR = Path("/home/user/project")
APP_YAML_PATH = PROJECT_DIR / "app.yaml"
PYPROJECT_TOML_PATH = PROJECT_DIR / "pyproject.toml"
README_PATH = PROJECT_DIR / "README.md"


@pytest.mark.describe("Initial directory structure")
def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Required project directory {PROJECT_DIR} is missing. "
        "The exercise should start with this directory present."
    )


@pytest.mark.describe("Initial app.yaml contents")
def test_app_yaml_initial_contents():
    assert APP_YAML_PATH.is_file(), (
        f"Expected YAML file not found at {APP_YAML_PATH}. "
        "The starter repository should include this file."
    )

    content = APP_YAML_PATH.read_text(encoding="utf-8")
    expected = (
        "services:\n"
        "  database:\n"
        "    host: localhost\n"
        "    port: 5432\n"
    )

    # Ensure the file matches exactly the expected starter text
    assert content == expected, (
        "The file /home/user/project/app.yaml does not match the expected "
        "initial contents.\n\n"
        "Expected:\n"
        f"{expected!r}\n\n"
        "Found:\n"
        f"{content!r}"
    )

    # Extra guard: make sure the logging section has NOT yet been inserted
    assert "logging:" not in content, (
        "The starter app.yaml must NOT contain a 'logging:' section yet. "
        "It will be added by the student."
    )


@pytest.mark.describe("Initial pyproject.toml contents")
def test_pyproject_toml_initial_contents():
    assert PYPROJECT_TOML_PATH.is_file(), (
        f"Expected TOML file not found at {PYPROJECT_TOML_PATH}. "
        "The starter repository should include this file."
    )

    content = PYPROJECT_TOML_PATH.read_text(encoding="utf-8")
    expected = (
        "[tool.poetry]\n"
        "name = \"tiny-util\"\n"
        "version = \"0.1.0\"\n"
        "description = \"Small helper scripts\"\n"
        "\n"
        "[tool.poetry.dependencies]\n"
        "python = \"^3.9\"\n"
    )

    assert content == expected, (
        "The file /home/user/project/pyproject.toml does not match the expected "
        "initial contents.\n\n"
        "Expected:\n"
        f"{expected!r}\n\n"
        "Found:\n"
        f"{content!r}"
    )

    # Ensure that the version has not already been bumped
    assert "version = \"0.2.0\"" not in content, (
        "pyproject.toml already shows version 0.2.0; it should start at 0.1.0."
    )


@pytest.mark.describe("README.md existence")
def test_readme_exists():
    assert README_PATH.is_file(), (
        "README.md should be present in the starter repository at "
        "/home/user/project/README.md."
    )