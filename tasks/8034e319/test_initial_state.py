# test_initial_state.py
#
# This pytest suite validates the state of the filesystem **before**
# the student makes any changes.  It checks only the files/directories
# that are supposed to exist initially and makes no assertions about
# any of the files or directories that will be created or modified
# later (per the task instructions and the “DO NOT test for any of the
# output files or directories” rule).

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
PROVISIONING_DIR = HOME / "provisioning"
CONFIG_DIR = PROVISIONING_DIR / "config"

APP_YML = CONFIG_DIR / "app.yml"
DB_TOML = CONFIG_DIR / "db.toml"


@pytest.fixture(scope="module")
def initial_app_yml_expected() -> str:
    """
    The exact contents (including the single trailing newline) that
    /home/user/provisioning/config/app.yml must have **before** the
    student performs any action.
    """
    return (
        "service:\n"
        "  name: webapp\n"
        "  port: 8000\n"
        "  debug: false\n"
    )


@pytest.fixture(scope="module")
def initial_db_toml_expected() -> str:
    """
    The exact contents (including the single trailing newline) that
    /home/user/provisioning/config/db.toml must have **before** the
    student performs any action.
    """
    return (
        "[connection]\n"
        'user = "admin"\n'
        'password = "secret"\n'
        'host = "localhost"\n'
        "port = 5432\n"
        "max_connections = 100\n"
    )


def test_directories_exist():
    """Ensure the required initial directories are present."""
    missing = [
        str(path)
        for path in (PROVISIONING_DIR, CONFIG_DIR)
        if not path.is_dir()
    ]
    assert not missing, (
        "The following required directory/directories are missing:\n  - "
        + "\n  - ".join(missing)
    )


@pytest.mark.parametrize(
    "path, desc",
    [
        (APP_YML, "/home/user/provisioning/config/app.yml"),
        (DB_TOML, "/home/user/provisioning/config/db.toml"),
    ],
)
def test_required_files_exist(path: Path, desc: str):
    """Ensure the required initial files are present."""
    assert path.is_file(), f"Required file missing: {desc}"


def test_app_yml_initial_content(initial_app_yml_expected: str):
    """Validate the exact initial content of app.yml, byte-for-byte."""
    content = APP_YML.read_text(encoding="utf-8")
    assert (
        content == initial_app_yml_expected
    ), (
        "/home/user/provisioning/config/app.yml content does not match "
        "the expected initial state.\n\n"
        "Expected:\n"
        "----------------\n"
        f"{initial_app_yml_expected!r}\n"
        "----------------\n"
        "Found:\n"
        "----------------\n"
        f"{content!r}\n"
        "----------------"
    )


def test_db_toml_initial_content(initial_db_toml_expected: str):
    """Validate the exact initial content of db.toml, byte-for-byte."""
    content = DB_TOML.read_text(encoding="utf-8")
    assert (
        content == initial_db_toml_expected
    ), (
        "/home/user/provisioning/config/db.toml content does not match "
        "the expected initial state.\n\n"
        "Expected:\n"
        "----------------\n"
        f"{initial_db_toml_expected!r}\n"
        "----------------\n"
        "Found:\n"
        "----------------\n"
        f"{content!r}\n"
        "----------------"
    )