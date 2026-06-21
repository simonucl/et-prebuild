# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student modifies anything.  It checks that the directory
# /home/user/artifactmgr exists with the two baseline configuration files
# (repos.yaml and settings.toml) in their expected “pre-task” form, and that
# no update.log file is present yet.

import pathlib
import textwrap
import pytest


ARTIFACT_ROOT = pathlib.Path("/home/user/artifactmgr")
REPOS_YAML = ARTIFACT_ROOT / "repos.yaml"
SETTINGS_TOML = ARTIFACT_ROOT / "settings.toml"
UPDATE_LOG = ARTIFACT_ROOT / "update.log"


# --------------------------------------------------------------------------- #
# Helper expectations (exact byte-for-byte strings, including final newlines) #
# --------------------------------------------------------------------------- #

EXPECTED_REPOS_YAML = textwrap.dedent(
    """\
    repositories:
      - name: core-libs
        url: https://artifacts.example.com/core-libs
        type: maven
      - name: dev-tools
        url: https://artifacts.example.com/dev-tools
        type: npm
      - name: graphics
        url: https://artifacts.example.com/graphics
        type: docker
    """
)

EXPECTED_SETTINGS_TOML = textwrap.dedent(
    """\
    [repository."core-libs"]
    autopublish = true

    [repository."dev-tools"]
    autopublish = false

    [repository."graphics"]
    autopublish = true
    """
)


# -------------------------- Tests for initial state ------------------------- #

def test_artifactmgr_directory_exists():
    assert ARTIFACT_ROOT.is_dir(), (
        f"Expected directory {ARTIFACT_ROOT} to exist, "
        "but it is missing or not a directory."
    )


def test_repos_yaml_initial_content():
    assert REPOS_YAML.is_file(), (
        f"Expected file {REPOS_YAML} to exist, but it is missing."
    )

    actual = REPOS_YAML.read_text(encoding="utf-8")
    assert actual == EXPECTED_REPOS_YAML, (
        f"{REPOS_YAML} does not match the expected initial contents.\n\n"
        "Hint: it must *not* contain the new 'edge-utils' repository yet.\n"
        "Diff (expected ⇢ actual):\n"
        f"--- expected\n+++ actual\n{_unified_diff(EXPECTED_REPOS_YAML, actual)}"
    )


def test_settings_toml_initial_content():
    assert SETTINGS_TOML.is_file(), (
        f"Expected file {SETTINGS_TOML} to exist, but it is missing."
    )

    actual = SETTINGS_TOML.read_text(encoding="utf-8")
    assert actual == EXPECTED_SETTINGS_TOML, (
        f"{SETTINGS_TOML} does not match the expected initial contents.\n\n"
        "Hint: it must *not* contain the new '[repository.\"edge-utils\"]' block yet.\n"
        "Diff (expected ⇢ actual):\n"
        f"--- expected\n+++ actual\n{_unified_diff(EXPECTED_SETTINGS_TOML, actual)}"
    )


def test_update_log_absent():
    assert not UPDATE_LOG.exists(), (
        f"{UPDATE_LOG} should NOT exist in the initial state, "
        "but a file was found."
    )


# --------------------------------------------------------------------------- #
# Internal utility: produce a short unified diff for easier debugging         #
# --------------------------------------------------------------------------- #
import difflib  # stdlib import placed after tests to satisfy “stdlib only”

def _unified_diff(expected: str, actual: str, n: int = 3) -> str:
    """
    Return a unified diff string (no trailing newline) between *expected* and
    *actual* limited to *n* context lines.  Used solely for clearer failure
    messages.
    """
    diff_lines = list(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            lineterm="",
            n=n,
        )
    )
    return "".join(diff_lines)