# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state that must be in place *before* the learner performs any action.
#
# What is expected to exist already:
#   • /home/user/data/                        (directory)
#   • /home/user/data/server_access.log       (file with 8 exact lines)
#
# What must NOT exist yet:
#   • /home/user/audit/                       (directory created later)
#   • /home/user/audit/dec2023_failed_login_ips.txt (final artefact)
#
# Any deviation means the starting point is wrong and the exercise cannot be
# evaluated correctly.

from pathlib import Path
import os
import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
ACCESS_LOG = DATA_DIR / "server_access.log"
AUDIT_DIR = HOME / "audit"
FINAL_FILE = AUDIT_DIR / "dec2023_failed_login_ips.txt"

EXPECTED_LOG_LINES = [
    "2023-12-02 08:15:43 INFO user1 192.168.1.10 SUCCESS LOGIN\n",
    "2023-12-02 08:16:10 WARN user2 10.0.0.5 FAILED LOGIN\n",
    "2023-12-02 09:00:01 WARN user5 172.16.0.3 FAILED LOGIN\n",
    "2023-11-30 18:12:00 WARN user9 10.0.0.5 FAILED LOGIN\n",
    "2023-12-15 12:22:17 WARN user6 192.168.1.10 FAILED LOGIN\n",
    "2023-12-20 10:55:00 INFO user3 10.0.0.5 SUCCESS LOGIN\n",
    "2023-12-20 11:00:14 WARN user2 10.0.0.5 FAILED LOGIN\n",
    "2023-12-31 23:59:59 WARN user7 203.0.113.1 FAILED LOGIN\n",
]


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory '{DATA_DIR}' is missing. "
        "The initial dataset must be located here."
    )


def test_access_log_exists_and_contents():
    assert ACCESS_LOG.is_file(), (
        f"Expected log file '{ACCESS_LOG}' is missing. "
        "It must be present *before* the exercise starts."
    )

    # Read the file in binary then decode with UTF-8 so that we can
    # detect exact newline characters without universal newlines masking.
    with ACCESS_LOG.open("rb") as fh:
        actual_bytes = fh.read()

    try:
        actual_text = actual_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"Log file '{ACCESS_LOG}' must be valid UTF-8. Decode error: {exc}"
        )

    expected_text = "".join(EXPECTED_LOG_LINES)
    assert actual_text == expected_text, (
        "The contents of 'server_access.log' do not match the expected initial "
        "fixture. Do **NOT** modify this file; it is the basis for grading.\n\n"
        "----- Expected -----\n"
        f"{expected_text}"
        "----- Actual -----\n"
        f"{actual_text}"
        "-------------------"
    )


def test_audit_directory_not_present_yet():
    # The grading instructions state that the learner/agent is responsible for
    # creating /home/user/audit and the artefact inside it.  Therefore at the
    # *initial* state they must not exist.
    assert not AUDIT_DIR.exists(), (
        f"Directory '{AUDIT_DIR}' already exists, but the exercise assumes it "
        "does not. Remove it so the learner can create it afresh."
    )


def test_final_artefact_not_present_yet():
    assert not FINAL_FILE.exists(), (
        f"Artefact '{FINAL_FILE}' already exists, but the exercise requires "
        "the learner to generate it. Remove it so grading starts from a clean "
        "state."
    )