# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present BEFORE the student carries out any actions described in the
# assignment.  It asserts that:
#
# 1. The sample repository exists under /home/user/project.
# 2. The two configuration files (app.conf, db.conf) and README.md exist
#    and contain exactly the expected contents.
# 3. No documentation artefacts that the student is supposed to create
#    yet exist (CONFIG_CHANGES.md and lint_pass.log).
#
# If any assertion fails the test log will make it clear what is missing
# or unexpected.

from pathlib import Path

import pytest


PROJECT_ROOT = Path("/home/user/project")
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"

APP_CONF_PATH = CONFIG_DIR / "app.conf"
DB_CONF_PATH = CONFIG_DIR / "db.conf"
README_PATH = PROJECT_ROOT / "README.md"
CONFIG_CHANGES_PATH = DOCS_DIR / "CONFIG_CHANGES.md"
LINT_PASS_LOG_PATH = DOCS_DIR / "lint_pass.log"


@pytest.fixture(scope="module")
def expected_app_conf():
    return (
        "# Application configuration\n"
        "ENABLE_FEATURE_X=false\n"
        "LOG_LEVEL=info\n"
    )


@pytest.fixture(scope="module")
def expected_db_conf():
    return (
        "# Database configuration\n"
        "max_connections=100\n"
        "shared_buffers=128MB\n"
    )


def test_project_directory_exists():
    assert PROJECT_ROOT.exists(), (
        f"Expected project directory {PROJECT_ROOT} to exist."
    )
    assert PROJECT_ROOT.is_dir(), (
        f"{PROJECT_ROOT} exists but is not a directory."
    )


def test_config_directory_exists():
    assert CONFIG_DIR.exists(), (
        f"Expected configuration directory {CONFIG_DIR} to exist."
    )
    assert CONFIG_DIR.is_dir(), (
        f"{CONFIG_DIR} exists but is not a directory."
    )


def test_app_conf_exists_and_contents(expected_app_conf):
    assert APP_CONF_PATH.exists(), (
        f"Missing file: {APP_CONF_PATH}"
    )
    file_text = APP_CONF_PATH.read_text()
    assert file_text == expected_app_conf, (
        f"Contents of {APP_CONF_PATH} differ from the expected template."
    )


def test_db_conf_exists_and_contents(expected_db_conf):
    assert DB_CONF_PATH.exists(), (
        f"Missing file: {DB_CONF_PATH}"
    )
    file_text = DB_CONF_PATH.read_text()
    assert file_text == expected_db_conf, (
        f"Contents of {DB_CONF_PATH} differ from the expected template."
    )


def test_readme_exists():
    assert README_PATH.exists(), (
        f"Missing README file: {README_PATH}"
    )
    assert README_PATH.is_file(), (
        f"{README_PATH} exists but is not a regular file."
    )


def test_docs_artifacts_do_not_yet_exist():
    # The docs directory itself may or may not exist; we only forbid the
    # target files that the student is supposed to create.
    assert not CONFIG_CHANGES_PATH.exists(), (
        f"{CONFIG_CHANGES_PATH} already exists, "
        "but it should NOT be present before the student runs their workflow."
    )
    assert not LINT_PASS_LOG_PATH.exists(), (
        f"{LINT_PASS_LOG_PATH} already exists, "
        "but it should NOT be present before the student runs their workflow."
    )