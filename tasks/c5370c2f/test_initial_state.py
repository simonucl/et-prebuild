# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student executes any command for the “artifact manager” task.
#
# The expectations are:
# 1. The configuration directory exists with 0755 permissions.
# 2. repo-settings.yaml exists, contains only the two original
#    repository blocks (core-libs and plugins) and *does not* contain
#    an experimental-tools block.
# 3. cleanup-policy.toml exists and still has `maxDays = 60`.
# 4. config-edit.log must **not** exist yet.
#
# If any of these assertions fail the student is starting from an
# unexpected state, so the exercise must be fixed before proceeding.

import os
import stat
import re
import pytest

BASE_DIR = "/home/user/repositories/config"
REPO_YAML = os.path.join(BASE_DIR, "repo-settings.yaml")
POLICY_TOML = os.path.join(BASE_DIR, "cleanup-policy.toml")
EDIT_LOG = os.path.join(BASE_DIR, "config-edit.log")


def _read(path: str) -> str:
    """Helper to read a text file, raise helpful error if missing."""
    if not os.path.exists(path):
        pytest.fail(f"Expected file '{path}' to exist but it is missing.")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as exc:
        pytest.fail(f"Could not read '{path}': {exc}")


def test_config_directory_exists_with_correct_permissions():
    assert os.path.isdir(BASE_DIR), f"Directory '{BASE_DIR}' does not exist."
    mode = stat.S_IMODE(os.stat(BASE_DIR).st_mode)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory '{BASE_DIR}' permissions are {oct(mode)}, "
        f"expected {oct(expected_mode)} (0755)."
    )


def test_repo_settings_initial_content():
    content = _read(REPO_YAML)

    # Must start with the expected header.
    assert content.lstrip().startswith("repositories:"), (
        f"'{REPO_YAML}' should start with 'repositories:' but does not."
    )

    # Ensure the original two blocks are present.
    for name in ("core-libs", "plugins"):
        pattern = rf'-\s+name:\s*"{name}"'
        assert re.search(pattern, content), (
            f"Original repository block for '{name}' is missing from '{REPO_YAML}'."
        )

    # The experimental-tools block MUST NOT yet be present.
    assert (
        'name: "experimental-tools"' not in content
    ), "The experimental-tools block is already present in repo-settings.yaml; initial state should not contain it."


def test_cleanup_policy_initial_content():
    content = _read(POLICY_TOML)

    # The policy table header must exist.
    assert "[policy]" in content, (
        f"'[policy]' section missing from '{POLICY_TOML}'."
    )

    # Ensure maxDays is exactly 60, not 45.
    # We use a regex to match the exact numeric value in the line.
    max_days_match = re.search(r"^\s*maxDays\s*=\s*(\d+)", content, re.MULTILINE)
    assert max_days_match, f"'maxDays' key not found in '{POLICY_TOML}'."
    current_value = int(max_days_match.group(1))
    assert current_value == 60, (
        f"Expected 'maxDays' to be 60 in '{POLICY_TOML}', "
        f"but found {current_value}."
    )


def test_edit_log_does_not_exist_yet():
    assert not os.path.exists(
        EDIT_LOG
    ), f"'{EDIT_LOG}' already exists, but it should be created only AFTER the student completes the task."