# test_initial_state.py
#
# Pytest suite that verifies the initial operating-system / filesystem state
# *before* the student rotates any credentials.
#
# Expected initial truth:
#   • Directory /home/user/secure exists.
#   • /home/user/secure/api_keys.txt exists and contains EXACTLY the
#     three lines below (LF line endings), in this order:
#         analytics:ABCD1234OLD
#         data-collector:XYZ7890OLD
#         monitoring:MON123OLD
#   • /home/user/secure/rotation.log must NOT exist yet.
#
# Only stdlib + pytest are used.

import os
import pathlib
import pytest

SECURE_DIR = pathlib.Path("/home/user/secure")
API_KEYS_FILE = SECURE_DIR / "api_keys.txt"
ROTATION_LOG = SECURE_DIR / "rotation.log"

EXPECTED_LINES = [
    "analytics:ABCD1234OLD",
    "data-collector:XYZ7890OLD",
    "monitoring:MON123OLD",
]


def _read_file_lines(path: pathlib.Path):
    """
    Helper: return list of lines without their trailing newline characters.
    Raises pytest failure if the file cannot be read.
    """
    try:
        with path.open("r", encoding="utf-8") as fh:
            # str.splitlines() discards the trailing '\n'
            return fh.read().splitlines()
    except FileNotFoundError:
        pytest.fail(f"Required file missing: {path}")
    except OSError as exc:
        pytest.fail(f"Could not read {path}: {exc}")


def test_secure_directory_exists():
    assert SECURE_DIR.is_dir(), (
        f"Directory {SECURE_DIR} is required but was not found."
    )


def test_api_keys_file_exists():
    assert API_KEYS_FILE.is_file(), (
        f"File {API_KEYS_FILE} is required but was not found."
    )


def test_api_keys_file_contents():
    lines = _read_file_lines(API_KEYS_FILE)

    assert len(lines) == len(EXPECTED_LINES), (
        f"{API_KEYS_FILE} should contain exactly {len(EXPECTED_LINES)} lines: "
        f"{EXPECTED_LINES}\nFound {len(lines)} lines instead: {lines}"
    )

    for idx, (found, expected) in enumerate(zip(lines, EXPECTED_LINES), start=1):
        assert found == expected, (
            f"Line {idx} of {API_KEYS_FILE} is incorrect.\n"
            f"Expected: {expected!r}\nFound:    {found!r}"
        )


def test_rotation_log_absent():
    assert not ROTATION_LOG.exists(), (
        f"{ROTATION_LOG} should NOT exist yet, "
        "but a file with that name was found."
    )