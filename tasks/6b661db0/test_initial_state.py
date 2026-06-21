# test_initial_state.py
#
# This pytest suite validates the operating-system state *before* the
# student begins work.  It checks that the required input directory and
# log file exist and that the log file’s contents match the canonical
# 10-line sample provided in the task description.
#
# NOTE:  The tests deliberately avoid looking for any artefacts that the
#        student is expected to create later (such as /home/user/ir_reports
#        or its contents).

from pathlib import Path
import pytest

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "auth_sample.log"

# The exact 10 lines expected to be present in auth_sample.log,
# each **without** a trailing newline.
EXPECTED_LINES = [
    "Jun 10 12:34:56 server sshd[1234]: Failed password for invalid user admin from 192.168.1.10 port 54321 ssh2",
    "Jun 10 12:35:01 server sshd[1235]: Failed password for root from 203.0.113.5 port 54322 ssh2",
    "Jun 10 12:35:05 server sshd[1236]: Failed password for invalid user guest from 192.168.1.10 port 54323 ssh2",
    "Jun 10 12:35:10 server sshd[1237]: Failed password for invalid user test from 198.51.100.25 port 54324 ssh2",
    "Jun 10 12:35:15 server sshd[1238]: Failed password for root from 203.0.113.5 port 54325 ssh2",
    "Jun 10 12:35:20 server sshd[1239]: Failed password for invalid user admin from 198.51.100.25 port 54326 ssh2",
    "Jun 10 12:35:25 server sshd[1240]: Failed password for invalid user admin from 192.168.1.10 port 54327 ssh2",
    "Jun 10 12:35:30 server sshd[1241]: Failed password for root from 203.0.113.5 port 54328 ssh2",
    "Jun 10 12:35:35 server sshd[1242]: Failed password for invalid user admin from 192.168.1.10 port 54329 ssh2",
    "Jun 10 12:35:40 server sshd[1243]: Failed password for invalid user guest from 192.0.2.44 port 54330 ssh2",
]


def test_log_directory_exists():
    """The /home/user/logs directory must exist and be a directory."""
    assert LOG_DIR.exists(), f"Required directory not found: {LOG_DIR}"
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory."


def test_log_file_exists():
    """The auth_sample.log file must exist and be a regular file."""
    assert LOG_FILE.exists(), (
        f"Expected log file not found: {LOG_FILE}\n"
        "Create the file with the exact name and path shown."
    )
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_log_file_contents_exact_match():
    """
    The log file must contain exactly the 10 canonical lines provided in the
    task description, using UNIX newlines and ending with a final newline.
    """
    raw_data = LOG_FILE.read_bytes()

    # 1. The file must end with a single '\n'.
    assert raw_data.endswith(b"\n"), (
        f"{LOG_FILE} must end with a single UNIX newline (LF)."
    )

    # 2. Decode safely as UTF-8 and split into lines (dropping the final '\n').
    text = raw_data.decode("utf-8")
    actual_lines = text.rstrip("\n").split("\n")

    # 3. Ensure the line count is exactly 10.
    assert len(actual_lines) == 10, (
        f"{LOG_FILE} should contain exactly 10 lines; "
        f"found {len(actual_lines)}."
    )

    # 4. Compare line-by-line with the canonical sample.
    mismatches = [
        (i + 1, exp, act)
        for i, (exp, act) in enumerate(zip(EXPECTED_LINES, actual_lines))
        if exp != act
    ]
    assert not mismatches, _format_mismatch_error(mismatches)


def _format_mismatch_error(mismatches):
    """
    Produce a detailed, human-readable explanation of any line mismatches
    to help the student correct the file.
    """
    lines = ["auth_sample.log does not match the expected contents:"]
    for lineno, exp, act in mismatches:
        lines.append(f"  Line {lineno}:")
        lines.append(f"    expected: {exp!r}")
        lines.append(f"    found   : {act!r}")
    return "\n".join(lines)