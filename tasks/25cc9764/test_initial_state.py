# test_initial_state.py
#
# This test-suite verifies the environment *before* the student starts
# working.  It makes sure that the only pre-existing artefact required
# for the exercise—the authentication log—exists in the right place and
# contains the exact bytes that the assignment specifies.
#
# NOTE:
# • We purposely do **not** test for the presence (or absence) of any
#   output artefacts such as “/home/user/report” or the final CSV,
#   because those belong to the *result* of the student’s work.
# • Only the Python standard library and pytest are used.

import io
from pathlib import Path
import pytest

AUTH_LOG_PATH = Path("/home/user/data/auth.log")

# The precise, byte-for-byte content that must already be present.
EXPECTED_AUTH_LOG_CONTENT = (
    "2023-05-14T08:14:22Z|admin|192.168.1.45|FAILED_LOGIN\n"
    "2023-05-14T08:14:26Z|john|192.168.1.23|SUCCESSFUL_LOGIN\n"
    "2023-05-14T08:15:02Z|root|10.0.0.15|FAILED_LOGIN\n"
    "2023-05-14T08:15:45Z|mary|192.168.1.23|SESSION_CLOSED\n"
    "2023-05-14T08:16:03Z|test|172.16.0.8|FAILED_LOGIN\n"
    "2023-05-14T08:16:48Z|john|192.168.1.23|SUDO_SESSION_OPENED\n"
)

@pytest.fixture(scope="module")
def auth_log_bytes():
    """
    Load the auth.log file as raw bytes and return them.

    The fixture fails early with a clear error message if the file is
    missing or inaccessible.
    """
    if not AUTH_LOG_PATH.exists():
        pytest.fail(
            f"Required source log missing: {AUTH_LOG_PATH!s}\n"
            "Make sure the file is in place before you begin."
        )
    if not AUTH_LOG_PATH.is_file():
        pytest.fail(
            f"Expected a regular file at {AUTH_LOG_PATH!s}, "
            "but something else was found."
        )
    try:
        # Open in binary mode to keep exact bytes for newline checks.
        return AUTH_LOG_PATH.read_bytes()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {AUTH_LOG_PATH!s}: {exc}")

def test_auth_log_exact_content(auth_log_bytes):
    """
    The log file must match the assignment spec *exactly*.

    We check:
    1. Pure LF line endings (no CR characters).
    2. Exactly the six expected lines, in order.
    3. A single trailing LF at the very end.
    """
    raw = auth_log_bytes

    # 1. No CR characters (Windows line breaks)
    assert b"\r" not in raw, (
        "The auth.log file contains carriage-return (CR) characters. "
        "It must use Unix LF (\\n) line endings only."
    )

    # 2 & 3. Exact byte-for-byte match
    expected_bytes = EXPECTED_AUTH_LOG_CONTENT.encode("utf-8")
    assert raw == expected_bytes, (
        "The content of /home/user/data/auth.log does not match the "
        "expected fixture.\n"
        "---- Expected ----\n"
        f"{EXPECTED_AUTH_LOG_CONTENT}\n"
        "------------------\n"
        "If the file was modified, restore it before proceeding."
    )

def test_auth_log_columns(auth_log_bytes):
    """
    Sanity-check each line contains exactly four '|'-separated columns.
    """
    text = auth_log_bytes.decode("utf-8")
    for idx, line in enumerate(io.StringIO(text), start=1):
        line = line.rstrip("\n")
        parts = line.split("|")
        assert len(parts) == 4, (
            f"Line {idx} of auth.log should have 4 columns separated by '|', "
            f"but {len(parts)} columns were found: {line!r}"
        )