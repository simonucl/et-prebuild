# test_initial_state.py
#
# This suite verifies the filesystem *before* the student carries out
# any actions.  It checks that the source log directory and its three
# files exist with the expected byte-for-byte contents.  It does **NOT**
# test for the deliverable artefacts because those are created later.

import os
from pathlib import Path

HOME = Path("/home/user")
API_LOG_DIR = HOME / "api_logs"

# Expected relative file names -> expected UTF-8 contents.
EXPECTED_FILES = {
    "errors.log": "[Error] 504 Gateway Timeout at 2023-02-01T12:34:56Z\n",
    "request.log": "GET /v1/data 200 OK\n",
    "response.log": (
        "HTTP/1.1 200 OK\n"
        "Content-Type: application/json\n"
        '{ "status": "ok" }\n'
    ),
}


def test_api_log_directory_exists_and_is_directory():
    """api_logs directory must exist and be a directory."""
    assert API_LOG_DIR.exists(), f"Required directory not found: {API_LOG_DIR}"
    assert API_LOG_DIR.is_dir(), f"Expected {API_LOG_DIR} to be a directory."


def _read_text_bytes(path: Path) -> bytes:
    """
    Read a file as raw bytes.
    We compare bytes instead of str to ensure *exact* byte-for-byte match,
    including newlines.
    """
    with path.open("rb") as fh:
        return fh.read()


def test_expected_log_files_exist_with_correct_content():
    """
    Each expected log file must exist directly inside /home/user/api_logs
    and contain the exact predefined content.
    """
    for rel_name, expected_content in EXPECTED_FILES.items():
        abs_path = API_LOG_DIR / rel_name
        assert abs_path.exists(), f"Missing required file: {abs_path}"
        assert abs_path.is_file(), f"Expected a regular file, but got something else: {abs_path}"

        actual_bytes = _read_text_bytes(abs_path)
        expected_bytes = expected_content.encode("utf-8")

        assert (
            actual_bytes == expected_bytes
        ), (
            f"File contents of {abs_path} do not match the expected value.\n"
            f"Expected bytes:\n{expected_bytes!r}\n\nActual bytes:\n{actual_bytes!r}"
        )


def test_no_unexpected_files_in_api_logs_directory():
    """
    Ensure that /home/user/api_logs contains *only* the three expected
    files and no extra items (files or sub-directories).
    """
    present_names = sorted(p.name for p in API_LOG_DIR.iterdir())
    expected_names = sorted(EXPECTED_FILES.keys())

    assert (
        present_names == expected_names
    ), (
        "The api_logs directory contains unexpected items.\n"
        f"Expected exactly: {expected_names}\n"
        f"Found instead:    {present_names}"
    )