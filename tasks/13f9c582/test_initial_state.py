# test_initial_state.py
#
# Pytest suite to validate the *initial* operating-system / filesystem
# state **before** the student performs any action.
#
# What we check:
# 1.  /home/user/logs  exists and is a directory.
# 2.  /home/user/logs/auth.log  exists and is a regular file.
# 3.  The contents of  auth.log  exactly match what the task description
#    promises, including final trailing newline.
# 4.  There are exactly six occurrences of the exact phrase
#    “Failed password” in the file, so that the follow-up exercise
#    makes sense.
#
# We deliberately do *not* look for the output directory or report
# file (/home/user/incident/…) because the student has not created
# them yet and the grading guidelines forbid such checks.

from pathlib import Path
import pytest

LOG_DIR = Path("/home/user/logs")
AUTH_LOG = LOG_DIR / "auth.log"

# The reference contents that must be present in /home/user/logs/auth.log
EXPECTED_AUTH_LOG_CONTENT = (
    "May 15 10:22:34 server sshd[12345]: Failed password for invalid user admin from 192.168.1.10 port 51122 ssh2\n"
    "May 15 10:23:01 server sshd[12346]: Failed password for root from 203.0.113.5 port 42311 ssh2\n"
    "May 15 10:24:07 server sshd[12347]: Accepted password for user1 from 192.0.2.7 port 38712 ssh2\n"
    "May 15 10:25:12 server sshd[12348]: Failed password for root from 203.0.113.5 port 42319 ssh2\n"
    "May 15 10:26:14 server sshd[12349]: Failed password for invalid user test from 198.51.100.55 port 53345 ssh2\n"
    "May 15 10:27:18 server sshd[12350]: Failed password for invalid user admin from 192.168.1.10 port 51159 ssh2\n"
    "May 15 10:28:30 server sshd[12351]: Accepted password for user2 from 203.0.113.8 port 42229 ssh2\n"
    "May 15 10:29:02 server sshd[12352]: Failed password for root from 203.0.113.8 port 42235 ssh2\n"
)

def _read_auth_log():
    """Helper that reads the auth.log file and returns its contents."""
    try:
        return AUTH_LOG.read_text(encoding="utf-8")
    except Exception as exc:
        pytest.fail(f"Unable to read {AUTH_LOG}: {exc}")

def test_logs_directory_exists():
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."

def test_auth_log_exists_and_is_file():
    assert AUTH_LOG.exists(), f"Required log file {AUTH_LOG} is missing."
    assert AUTH_LOG.is_file(), f"{AUTH_LOG} exists but is not a regular file."

def test_auth_log_exact_contents():
    """Auth log must match the exact expected contents (byte-for-byte)."""
    contents = _read_auth_log()
    assert contents == EXPECTED_AUTH_LOG_CONTENT, (
        "The contents of /home/user/logs/auth.log do not match the expected "
        "reference data. Ensure the file has not been modified and contains "
        "exactly the eight lines specified in the task description, each "
        "terminated by a newline."
    )

def test_failed_password_count():
    """Sanity-check the number of 'Failed password' lines is exactly six."""
    contents = _read_auth_log()
    failed_lines = [ln for ln in contents.splitlines() if "Failed password" in ln]
    assert len(failed_lines) == 6, (
        "The auth.log file should contain exactly 6 lines with the phrase "
        "'Failed password' so the follow-up counting task produces the "
        "expected number. Found "
        f"{len(failed_lines)} such lines instead."
    )