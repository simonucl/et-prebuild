# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system state is
# exactly as described in the task instructions.  It purposefully does **not**
# test for any artefacts that the student is supposed to create later
# (e.g. /home/user/app/security/failed_ssh_ips.txt); it only checks the
# pre-existing environment.

import os
import stat
import textwrap
import pytest

HOME = "/home/user"
APP_DIR = os.path.join(HOME, "app")
LOGS_DIR = os.path.join(APP_DIR, "logs")
ACCESS_LOG = os.path.join(LOGS_DIR, "access.log")


@pytest.fixture(scope="module")
def access_log_contents():
    """Return the full contents of the reference access.log file."""
    with open(ACCESS_LOG, encoding="utf-8") as fh:
        return fh.read()


def test_app_directory_exists():
    assert os.path.isdir(APP_DIR), (
        f"Expected directory {APP_DIR!r} to exist."
    )
    # Mode check ─ only the permission bits (e.g. 0o755)
    mode = stat.S_IMODE(os.stat(APP_DIR).st_mode)
    assert mode == 0o755, (
        f"Directory {APP_DIR!r} should have mode 755, found {oct(mode)}."
    )


def test_logs_directory_exists():
    assert os.path.isdir(LOGS_DIR), (
        f"Expected directory {LOGS_DIR!r} to exist."
    )
    mode = stat.S_IMODE(os.stat(LOGS_DIR).st_mode)
    assert mode == 0o755, (
        f"Directory {LOGS_DIR!r} should have mode 755, found {oct(mode)}."
    )


def test_access_log_file_exists_and_mode():
    assert os.path.isfile(ACCESS_LOG), (
        f"Expected log file {ACCESS_LOG!r} to exist."
    )
    mode = stat.S_IMODE(os.stat(ACCESS_LOG).st_mode)
    assert mode == 0o644, (
        f"File {ACCESS_LOG!r} should have mode 644, found {oct(mode)}."
    )


def test_access_log_contents_exact(access_log_contents):
    expected = textwrap.dedent(
        """\
        Aug 11 15:12:32 server sshd[1234]: Failed password for invalid user admin from 192.0.2.10 port 51158 ssh2
        Aug 11 15:13:00 server sshd[1235]: Failed password for root from 198.51.100.23 port 51234 ssh2
        Aug 11 15:13:15 server sshd[1236]: Failed password for invalid user test from 192.0.2.10 port 51376 ssh2
        Aug 11 15:14:22 server sshd[1237]: Failed password for root from 203.0.113.7 port 51455 ssh2
        Aug 11 15:14:50 server sshd[1238]: Accepted password for alice from 198.51.100.34 port 51477 ssh2
        Aug 11 15:15:05 server sshd[1239]: Connection closed by authenticating user bob 203.0.113.8 port 51501 [preauth]
        """
    )
    # The canonical file must include the final newline.
    assert access_log_contents == expected, (
        f"Contents of {ACCESS_LOG!r} do not match the expected initial "
        "SSH access log."
    )