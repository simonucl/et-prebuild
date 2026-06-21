# test_initial_state.py
#
# This pytest suite verifies the _initial_ state of the operating system /
# filesystem before the student performs any credential-rotation steps.
#
# It checks that:
#   • the three expected *.cfg files exist under /home/user/infra/
#   • each file contains the correct 2022-based credentials (and nothing else)
#   • the consolidated JSON file and the rotation log do NOT yet exist
#
# The tests purposefully fail with clear, actionable messages if the starting
# state is incorrect.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
INFRA_DIR = HOME / "infra"

CFG_EXPECTATIONS = {
    "db.cfg": {
        "username": "db_user",
        "password": "db_pass_2022",
    },
    "redis.cfg": {
        "username": "redis_user",
        "password": "redis_pass_2022",
    },
    "api.cfg": {
        "username": "api_user",
        "password": "api_pass_2022",
    },
}

CREDENTIALS_JSON_PATH = INFRA_DIR / "credentials.json"
ROTATION_LOG_PATH = HOME / "rotation.log"


def _read_file_lines(path: pathlib.Path):
    """Return the file's lines exactly as stored (including the trailing '\n')."""
    with path.open("r", encoding="utf-8") as f:
        return f.readlines()


def test_infra_directory_exists():
    assert INFRA_DIR.exists(), f"Required directory {INFRA_DIR} not found."
    assert INFRA_DIR.is_dir(), f"{INFRA_DIR} exists but is not a directory."


@pytest.mark.parametrize("cfg_name,expected", CFG_EXPECTATIONS.items())
def test_cfg_files_exist_with_expected_content(cfg_name, expected):
    cfg_path = INFRA_DIR / cfg_name
    assert cfg_path.exists(), f"Expected file {cfg_path} is missing."
    assert cfg_path.is_file(), f"{cfg_path} exists but is not a regular file."

    lines = _read_file_lines(cfg_path)

    # Each *.cfg* file must have exactly two newline-terminated lines.
    assert len(lines) == 2, (
        f"{cfg_path} should contain exactly two lines (username/password) "
        f"but contains {len(lines)} line(s): {lines!r}"
    )

    username_line, password_line = lines

    expected_username_line = f"username={expected['username']}\n"
    expected_password_line = f"password={expected['password']}\n"

    assert username_line == expected_username_line, (
        f"{cfg_path} username line mismatch:\n"
        f"  expected: {expected_username_line!r}\n"
        f"  found:    {username_line!r}"
    )
    assert password_line == expected_password_line, (
        f"{cfg_path} password line mismatch:\n"
        f"  expected: {expected_password_line!r}\n"
        f"  found:    {password_line!r}"
    )


def test_credentials_json_not_present_yet():
    assert not CREDENTIALS_JSON_PATH.exists(), (
        f"{CREDENTIALS_JSON_PATH} should NOT exist before rotation starts."
    )


def test_rotation_log_not_present_yet():
    # The specification implies the log may or may not exist historically.
    # We only enforce that the three new lines are NOT already present,
    # because they must be appended by the student later.
    if not ROTATION_LOG_PATH.exists():
        # Ideal initial state: no log file at all.
        return

    # If the file does exist, ensure the 2025 entries are not already there.
    with ROTATION_LOG_PATH.open("r", encoding="utf-8") as f:
        content = f.read()

    forbidden_substrings = [
        "db_pass_2025",
        "redis_pass_2025",
        "api_pass_2025",
    ]
    for substr in forbidden_substrings:
        assert substr not in content, (
            f"{ROTATION_LOG_PATH} already contains '{substr}'. "
            "The rotation lines must be added later, not pre-existing."
        )