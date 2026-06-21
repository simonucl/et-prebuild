# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student performs any actions.
#
# What we verify (and nothing more):
# 1. /home/user/sample_logs exists and is a directory.
# 2. /home/user/sample_logs/system.log exists and is a regular, readable file.
# 3. system.log contains **exactly** the eight expected lines (including order
#    and text), and there are exactly six “Failed password” lines.
#
# NOTE:  We deliberately do *not* test for the presence or absence of any
#        deliverable paths such as /home/user/incident_scan, as per the rules.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
SAMPLE_DIR = HOME / "sample_logs"
SYSTEM_LOG = SAMPLE_DIR / "system.log"

EXPECTED_LINES = [
    "Jul 10 11:23:56 server sshd[2345]: Failed password for invalid user admin from 10.0.0.55 port 54322 ssh2",
    "Jul 10 11:23:58 server sshd[2346]: Failed password for invalid user admin from 10.0.0.55 port 54323 ssh2",
    "Jul 10 11:24:02 server sshd[2347]: Accepted password for user1 from 192.168.1.10 port 54411 ssh2",
    "Jul 10 11:25:01 server sshd[2348]: Failed password for invalid user root from 203.0.113.99 port 51720 ssh2",
    "Jul 10 11:25:13 server sshd[2351]: Failed password for root from 203.0.113.99 port 51721 ssh2",
    "Jul 10 11:26:30 server sshd[2355]: Failed password for invalid user admin from 10.0.0.55 port 54324 ssh2",
    "Jul 10 11:27:00 server cron[1111]: pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
    "Jul 10 11:28:45 server sshd[2359]: Failed password for root from 198.51.100.77 port 51800 ssh2",
]


def test_sample_logs_dir_exists():
    assert SAMPLE_DIR.exists(), (
        f"Required directory {SAMPLE_DIR} is missing. "
        "Create it before running any further tasks."
    )
    assert SAMPLE_DIR.is_dir(), f"{SAMPLE_DIR} exists but is not a directory."


def test_system_log_exists_and_readable():
    assert SYSTEM_LOG.exists(), (
        f"Required log file {SYSTEM_LOG} is missing. "
        "Ensure the file is present with the expected contents."
    )
    assert SYSTEM_LOG.is_file(), f"{SYSTEM_LOG} exists but is not a regular file."
    # Basic readability check
    try:
        SYSTEM_LOG.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Cannot read {SYSTEM_LOG}: {exc}")


def test_system_log_contents():
    content = SYSTEM_LOG.read_text(encoding="utf-8")
    # Ensure the file ends with a newline so we know lines are complete.
    assert content.endswith(
        "\n"
    ), f"{SYSTEM_LOG} must end with a trailing newline (\\n)."

    lines = content.rstrip("\n").split("\n")  # remove final newline, keep others
    assert (
        lines == EXPECTED_LINES
    ), (
        f"{SYSTEM_LOG} does not contain the expected contents.\n"
        "Differences:\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n"
        + "\n".join(EXPECTED_LINES)
        + "\n\nActual ({len(lines)} lines):\n"
        + "\n".join(lines)
    )

    # Additional sanity check: count of 'Failed password' lines
    failed_lines = [ln for ln in lines if "Failed password" in ln]
    assert len(failed_lines) == 6, (
        f"Expected 6 lines containing 'Failed password' but found "
        f"{len(failed_lines)}. Verify the log contents."
    )