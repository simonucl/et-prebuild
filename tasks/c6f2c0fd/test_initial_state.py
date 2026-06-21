# test_initial_state.py
#
# This pytest module verifies the *initial* operating-system state
# before the student starts making changes.  It confirms:
#   1. The sample payloads directory and files exist with the exact
#      contents and byte-sizes specified in the task description.
#   2. No /home/user/api_tests directory is present yet.
#
# Only Python’s standard library and pytest are used.

import os
import stat
import pytest

SAMPLE_DIR = "/home/user/sample_payloads"
API_TESTS_DIR = "/home/user/api_tests"

# Expected payloads: (relative filename, absolute path, expected bytes-content)
EXPECTED_PAYLOADS = [
    (
        "user_create.json",
        os.path.join(SAMPLE_DIR, "user_create.json"),
        b'{"user":{"id":0,"name":"Alice"}}\n',   # 33 bytes
    ),
    (
        "order_create.json",
        os.path.join(SAMPLE_DIR, "order_create.json"),
        b'{"order":{"id":0,"item":"Widget","quantity":3}}\n',  # 48 bytes
    ),
]


def _human_readable_size(size: int) -> str:
    """Return a human readable string for an integer byte size."""
    return f"{size} byte{'s' if size != 1 else ''}"


def test_sample_payloads_directory_exists_and_is_directory():
    """Verify that /home/user/sample_payloads exists and is a directory."""
    assert os.path.isdir(
        SAMPLE_DIR
    ), f"Required directory {SAMPLE_DIR!r} is missing or is not a directory."


@pytest.mark.parametrize("filename, abs_path, expected_bytes", EXPECTED_PAYLOADS)
def test_sample_payload_file_exists_and_has_exact_content(filename, abs_path, expected_bytes):
    """
    Verify that each sample payload file exists, has correct permissions
    (is a regular file), exact byte size, and exact byte-for-byte content.
    """
    # 1. Presence and type
    assert os.path.exists(
        abs_path
    ), f"Expected sample payload {abs_path!r} is missing."
    st = os.stat(abs_path)
    assert stat.S_ISREG(
        st.st_mode
    ), f"Expected sample payload {abs_path!r} is not a regular file."

    # 2. Size
    expected_size = len(expected_bytes)
    actual_size = st.st_size
    assert (
        actual_size == expected_size
    ), (
        f"Sample payload {filename!r} has size {_human_readable_size(actual_size)}, "
        f"but {_human_readable_size(expected_size)} was expected."
    )

    # 3. Exact content
    with open(abs_path, "rb") as fp:
        data = fp.read()
    assert (
        data == expected_bytes
    ), f"Content of {filename!r} does not match the expected bytes."


def test_api_tests_directory_does_not_exist_yet():
    """
    Before the student begins, the /home/user/api_tests directory should NOT exist.
    """
    assert not os.path.exists(
        API_TESTS_DIR
    ), (
        f"Directory {API_TESTS_DIR!r} should NOT exist before the task is started, "
        "but it does."
    )