# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# before the student performs any actions for the localization task.
#
# It checks that the two configuration files already provided by the
# exercise exist and contain exactly the expected initial contents.
#
# NOTE:
# • We purposely do NOT look for /home/user/update_log.txt or for the
#   Spanish section in translations.yml, because those belong to the
#   *target* state that the student must create.
# • All absolute paths are used, in accordance with the grading rules.

import os
import textwrap
import pytest

PROJECT_DIR = "/home/user/project"
TRANSLATIONS_PATH = os.path.join(PROJECT_DIR, "translations.yml")
SETTINGS_PATH = os.path.join(PROJECT_DIR, "settings.toml")


@pytest.fixture(scope="module")
def translations_content():
    """Read the translations.yml file once for all tests."""
    if not os.path.isfile(TRANSLATIONS_PATH):
        pytest.fail(
            f"Expected file {TRANSLATIONS_PATH!r} to exist, but it is missing."
        )
    with open(TRANSLATIONS_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def settings_content():
    """Read the settings.toml file once for all tests."""
    if not os.path.isfile(SETTINGS_PATH):
        pytest.fail(
            f"Expected file {SETTINGS_PATH!r} to exist, but it is missing."
        )
    with open(SETTINGS_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


def test_project_directory_exists():
    assert os.path.isdir(
        PROJECT_DIR
    ), f"Directory {PROJECT_DIR!r} is missing—did you clone the project correctly?"


def test_translations_initial_content(translations_content):
    """
    The initial translations.yml must contain only English and French blocks,
    with 2-space indentation, and must not yet contain the Spanish section.
    """
    expected = textwrap.dedent(
        """\
        en:
          login: "Login"
          logout: "Logout"

        fr:
          login: "Connexion"
          logout: "Déconnexion"
        """
    )

    # Compare normalized content (strip trailing whitespace & newlines).
    assert translations_content.strip() == expected.strip(), (
        "The contents of translations.yml do not match the expected initial state.\n"
        "Make sure you have not already added the Spanish section or modified "
        "the existing keys."
    )

    assert (
        "es:" not in translations_content
    ), "translations.yml already contains an 'es:' block, but it should NOT be there yet."


def test_settings_initial_content(settings_content):
    """
    The initial settings.toml must set default_locale to 'en_US'
    and fallback_locale to 'en_US'.
    """
    expected = textwrap.dedent(
        """\
        [localization]
        default_locale = "en_US"
        fallback_locale = "en_US"
        """
    )

    assert settings_content.strip() == expected.strip(), (
        "settings.toml content does not match the expected initial state.\n"
        "Ensure default_locale is still 'en_US' and fallback_locale is unchanged."
    )