# test_initial_state.py
#
# This pytest suite validates that the workstation is in the EXPECTED
# *initial* state ­– before the student performs any edits.  It checks:
#
# 1. The presence and permissions of /home/user/build_configs.
# 2. The presence, permissions, and exact content of the two configuration
#    files that the student is expected to modify.
#
# NOTE: The suite intentionally avoids looking for (or at) any files that
# will be created *after* the student completes the task (e.g.,
# build_update.log).

import os
import stat
import pytest

BASE_DIR = "/home/user/build_configs"
APP_YAML = os.path.join(BASE_DIR, "app.yaml")
RELEASE_TOML = os.path.join(BASE_DIR, "release.toml")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mode(path):
    """Return the permission bits (e.g., 0o644) for the given path."""
    return stat.S_IMODE(os.stat(path).st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_build_configs_directory_exists_and_mode():
    assert os.path.isdir(BASE_DIR), (
        f"Directory {BASE_DIR} is missing. It must exist before the exercise begins."
    )
    expected_mode = 0o755
    actual_mode = _mode(BASE_DIR)
    assert actual_mode == expected_mode, (
        f"Directory {BASE_DIR} exists but has permissions {oct(actual_mode)}; "
        f"expected {oct(expected_mode)}."
    )


def test_app_yaml_exists_and_mode():
    assert os.path.isfile(APP_YAML), (
        f"Required file {APP_YAML} is missing."
    )
    expected_mode = 0o644
    actual_mode = _mode(APP_YAML)
    assert actual_mode == expected_mode, (
        f"{APP_YAML} has permissions {oct(actual_mode)}; expected {oct(expected_mode)}."
    )


def test_app_yaml_initial_content():
    """
    app.yaml must initially contain exactly two lines:
        name: sample-app
        version: "1.2.3"
    (A trailing newline after the second line is acceptable.)
    """
    with open(APP_YAML, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    expected_lines = [
        "name: sample-app",
        'version: "1.2.3"',
    ]

    assert lines == expected_lines, (
        f"{APP_YAML} content mismatch.\n"
        f"Expected lines:\n{expected_lines}\n\n"
        f"Actual lines:\n{lines}"
    )


def test_release_toml_exists_and_mode():
    assert os.path.isfile(RELEASE_TOML), (
        f"Required file {RELEASE_TOML} is missing."
    )
    expected_mode = 0o644
    actual_mode = _mode(RELEASE_TOML)
    assert actual_mode == expected_mode, (
        f"{RELEASE_TOML} has permissions {oct(actual_mode)}; expected {oct(expected_mode)}."
    )


def test_release_toml_initial_content():
    """
    release.toml must initially contain the following exact five non-empty lines
    (plus blank separators) in this order:

        [build]
        number = 102

        [metadata]
        checksum = ""

    The blank line between the two sections is required. Trailing newlines
    after the final line are acceptable.
    """
    with open(RELEASE_TOML, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    expected_lines = [
        "[build]",
        "number = 102",
        "",
        "[metadata]",
        'checksum = ""',
    ]

    assert lines == expected_lines, (
        f"{RELEASE_TOML} content mismatch.\n"
        f"Expected lines:\n{expected_lines}\n\n"
        f"Actual lines:\n{lines}"
    )