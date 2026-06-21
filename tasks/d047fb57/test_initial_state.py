# test_initial_state.py
#
# Pytest suite that validates the **initial** OS / filesystem state
# before the student performs any actions for the “SSH log filtering”
# exercise.
#
# Only the pre-existing artefact `/home/user/logs/auth.log`
# is verified; nothing related to the expected **output** directory
# (/home/user/filtered_logs) is touched here, in line with the
# “no-output-files” testing rule.

import pathlib
import pytest

AUTH_LOG_PATH = pathlib.Path("/home/user/logs/auth.log")


@pytest.fixture(scope="module")
def auth_log_lines():
    """
    Return the auth.log content split into lines (with their
    terminating newlines preserved).  The fixture fails early if the
    file is missing or not a regular file.
    """
    if not AUTH_LOG_PATH.exists():
        pytest.fail(
            f"Pre-existing log file absent: {AUTH_LOG_PATH!s} does not exist.",
            pytrace=False,
        )
    if not AUTH_LOG_PATH.is_file():
        pytest.fail(
            f"Expected {AUTH_LOG_PATH!s} to be a regular file, "
            f"but it is not.",
            pytrace=False,
        )

    # Read as UTF-8 text; the sample only contains ASCII characters.
    with AUTH_LOG_PATH.open("r", encoding="utf-8") as fh:
        lines = fh.read().splitlines(keepends=True)

    return lines


def test_auth_log_has_expected_number_of_lines(auth_log_lines):
    """
    The starter auth.log must contain exactly 10 lines.
    """
    assert len(auth_log_lines) == 10, (
        "auth.log should contain exactly 10 lines in the starter state; "
        f"found {len(auth_log_lines)}."
    )


def test_auth_log_exact_content(auth_log_lines):
    """
    Verify that auth.log matches the canonical baseline provided in the
    exercise description, byte-for-byte (including terminating newlines).
    """
    expected_lines = [
        "Jan 10 09:00:01 server sshd[12345]: Accepted password for alice from 192.168.1.10 port 53422 ssh2\n",
        "Jan 10 09:02:15 server sshd[12346]: Failed password for invalid user root from 203.0.113.1 port 61123 ssh2\n",
        "Jan 10 09:05:47 server sshd[12347]: Failed password for bob from 192.168.1.11 port 51234 ssh2\n",
        "Jan 10 09:07:32 server sshd[12348]: Accepted password for charlie from 192.168.1.12 port 55211 ssh2\n",
        "Jan 10 09:10:09 server sshd[12349]: Failed password for invalid user admin from 203.0.113.2 port 62345 ssh2\n",
        "Jan 10 09:15:55 server sshd[12350]: Accepted password for alice from 192.168.1.10 port 53445 ssh2\n",
        "Jan 10 09:20:16 server sshd[12351]: Failed password for dave from 192.168.1.13 port 50001 ssh2\n",
        "Jan 10 09:25:45 server sshd[12352]: Failed password for invalid user test from 203.0.113.3 port 63211 ssh2\n",
        "Jan 10 09:30:12 server sshd[12353]: Accepted password for bob from 192.168.1.11 port 51333 ssh2\n",
        "Jan 10 09:35:24 server sshd[12354]: Received disconnect from 192.168.1.12 port 55211:11: disconnected by user\n",
    ]

    assert auth_log_lines == expected_lines, (
        "The contents of /home/user/logs/auth.log do not match the "
        "expected baseline provided in the exercise description."
    )


def test_auth_log_failed_and_accepted_counts(auth_log_lines):
    """
    Sanity-check that the baseline file contains 5 “Failed password”
    lines and 4 “Accepted password” lines, as stated in the task
    description.  This ensures students will obtain the advertised
    counts once they implement the filters.
    """
    failed_lines = [ln for ln in auth_log_lines if "Failed password" in ln]
    accepted_lines = [ln for ln in auth_log_lines if "Accepted password" in ln]

    assert len(failed_lines) == 5, (
        "auth.log should contain exactly 5 lines with the substring "
        "'Failed password'; found "
        f"{len(failed_lines)}."
    )
    assert len(accepted_lines) == 4, (
        "auth.log should contain exactly 4 lines with the substring "
        "'Accepted password'; found "
        f"{len(accepted_lines)}."
    )