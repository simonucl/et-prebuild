# test_initial_state.py
#
# Pytest suite to verify the **initial** state of the operating system
# before the learner begins working on the “API-level connectivity” task.
#
# What we check (and ONLY what we check):
#   1. The directory /home/user/mock_api exists and is a directory.
#   2. The directory is accessible (read & execute bits for the user).
#   3. The file  /home/user/mock_api/ok.json exists.
#   4. The file’s content is exactly: {"status":"ok"}\n
#
# We intentionally do **NOT** look for any of the artefacts the student
# is expected to create later (/home/user/connectivity_logs, log files,
# running web servers, etc.).  This keeps the tests focused on the
# pre-exercise environment only.

import os
import stat
from pathlib import Path

import pytest


MOCK_API_DIR = Path("/home/user/mock_api")
OK_JSON_FILE = MOCK_API_DIR / "ok.json"
OK_JSON_EXPECTED_CONTENT = '{"status":"ok"}\n'


def _mode_bits(path: Path) -> int:
    """
    Helper: return Unix permission bits (the final 3 octal digits)
    for the given path.
    """
    return stat.S_IMODE(os.lstat(path).st_mode)


@pytest.mark.dependency(name="mock_api_dir_exists")
def test_mock_api_directory_exists():
    """
    The directory /home/user/mock_api must already exist and be a
    directory.  It should be readable and traversable by the current
    user (r-x------ minimum).
    """
    assert MOCK_API_DIR.exists(), (
        f"Expected directory {MOCK_API_DIR} to exist, but it does not."
    )
    assert MOCK_API_DIR.is_dir(), (
        f"{MOCK_API_DIR} exists but is not a directory."
    )

    mode = _mode_bits(MOCK_API_DIR)
    # Check owner read (0400) and execute (0100) bits are set.
    readable = bool(mode & stat.S_IRUSR)
    executable = bool(mode & stat.S_IXUSR)
    assert readable and executable, (
        f"{MOCK_API_DIR} permissions are {oct(mode)}; "
        "expected at least owner read (r) and execute (x) bits."
    )


@pytest.mark.dependency(depends=["mock_api_dir_exists"])
def test_ok_json_file_exists():
    """
    The file /home/user/mock_api/ok.json must already exist.
    """
    assert OK_JSON_FILE.exists(), (
        f"Expected file {OK_JSON_FILE} to exist, but it does not."
    )
    assert OK_JSON_FILE.is_file(), (
        f"{OK_JSON_FILE} exists but is not a regular file."
    )


@pytest.mark.dependency(depends=["mock_api_dir_exists"])
def test_ok_json_file_content_exact():
    """
    The content of ok.json must be exactly '{"status":"ok"}\\n'
    (including the trailing newline).
    """
    try:
        content = OK_JSON_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(
            f"Cannot read {OK_JSON_FILE}: file is missing."
        )
    except PermissionError:
        pytest.fail(
            f"Cannot read {OK_JSON_FILE}: permission denied."
        )

    assert content == OK_JSON_EXPECTED_CONTENT, (
        f"Unexpected content in {OK_JSON_FILE}.\n"
        f"Expected: {repr(OK_JSON_EXPECTED_CONTENT)}\n"
        f"Found:    {repr(content)}"
    )