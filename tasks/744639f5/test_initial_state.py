# test_initial_state.py
#
# This test-suite verifies the *initial* configuration state that must be
# present **before** the student starts working on the refactor task.
#
# It checks only the existing input files:
#   • /home/user/configs/app.yml
#   • /home/user/configs/db.toml
#
# It intentionally does NOT look for any of the output artefacts that the
# student will create later (combined.yml, changes.log, etc.).
#
# The tests rely exclusively on the Python standard library plus pytest.

import os
import textwrap
import pytest
from pathlib import Path

CONFIG_DIR = Path("/home/user/configs")
APP_YML   = CONFIG_DIR / "app.yml"
DB_TOML   = CONFIG_DIR / "db.toml"


def _normalise(text: str) -> list[str]:
    """
    Helper to provide a newline- and trailing-space-agnostic comparison.
    Returns a list of lines with trailing whitespace stripped.
    """
    # .strip() trims possible leading/trailing blank lines including final \n
    return [ln.rstrip() for ln in text.strip().splitlines()]


@pytest.fixture(scope="session")
def expected_app_content() -> list[str]:
    raw = textwrap.dedent(
        """\
        app_name: SampleApp
        debug: true
        version: 2.0.3
        database:
          host: localhost
          port: 5432
        """
    )
    return _normalise(raw)


@pytest.fixture(scope="session")
def expected_db_content() -> list[str]:
    raw = textwrap.dedent(
        """\
        [connection]
        host = "localhost"
        port = 5432
        user = "appuser"

        [settings]
        max_connections = 150
        """
    )
    return _normalise(raw)


def test_configs_directory_exists():
    assert CONFIG_DIR.is_dir(), (
        "The directory '/home/user/configs/' is missing. "
        "Create it before starting the refactor task."
    )


def test_app_yml_exists_and_is_correct(expected_app_content):
    assert APP_YML.is_file(), (
        "The file '/home/user/configs/app.yml' is missing. "
        "It must be present in its original state before modifications begin."
    )

    with APP_YML.open("r", encoding="utf-8") as fh:
        current_lines = _normalise(fh.read())

    assert current_lines == expected_app_content, (
        "The initial contents of '/home/user/configs/app.yml' do not match the "
        "expected starting point.\n\n"
        f"Expected:\n{os.linesep.join(expected_app_content)}\n\n"
        f"Found:\n{os.linesep.join(current_lines)}"
    )


def test_db_toml_exists_and_is_correct(expected_db_content):
    assert DB_TOML.is_file(), (
        "The file '/home/user/configs/db.toml' is missing. "
        "It must be present in its original state before modifications begin."
    )

    with DB_TOML.open("r", encoding="utf-8") as fh:
        current_lines = _normalise(fh.read())

    assert current_lines == expected_db_content, (
        "The initial contents of '/home/user/configs/db.toml' do not match the "
        "expected starting point.\n\n"
        f"Expected:\n{os.linesep.join(expected_db_content)}\n\n"
        f"Found:\n{os.linesep.join(current_lines)}"
    )