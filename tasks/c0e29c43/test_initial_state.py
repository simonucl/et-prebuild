# test_initial_state.py
#
# Pytest suite that validates the machine **before** the learner creates
# /home/user/dns_report.log.  These tests guarantee that:
#   1. The homework directory (/home/user) exists.
#   2. The report file does *not* yet exist (nothing has been done).
#   3. Forward and reverse DNS look-ups for the current hostname succeed.
#
# Only the Python stdlib and pytest are used.

import os
import re
import subprocess
from pathlib import Path

import pytest


HOME_DIR = Path("/home/user")
REPORT_FILE = HOME_DIR / "dns_report.log"

# Simple IPv4 regular expression (0–255 is not enforced; that is fine here)
IPV4_RE = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")


def _run(cmd):
    """
    Helper that executes `cmd` (list of str) and returns stdout stripped.
    Fails the test immediately if the command cannot be executed.
    """
    try:
        completed = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        pytest.fail(f"Required command not found: {cmd[0]!r}", pytrace=False)
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Command {' '.join(cmd)!r} exited with {exc.returncode}. "
            f"stderr was:\n{exc.stderr}",
            pytrace=False,
        )
    output = completed.stdout.strip()
    if not output:
        pytest.fail(f"No output from command: {' '.join(cmd)!r}", pytrace=False)
    return output


def test_home_directory_exists():
    assert HOME_DIR.is_dir(), (
        f"Expected home directory {HOME_DIR} to exist and be a directory, "
        "but it was not found."
    )


def test_dns_report_file_does_not_exist_yet():
    assert not REPORT_FILE.exists(), (
        f"{REPORT_FILE} already exists, but it should **not** be present "
        "before the learner runs their solution."
    )


def test_hostname_resolves_forward_and_reverse():
    # 1. Obtain the runtime hostname
    hostname = _run(["hostname"]).splitlines()[0]
    assert hostname, "The system 'hostname' command returned an empty string."

    # 2. Forward lookup: getent hosts <hostname>
    forward_line = _run(["getent", "hosts", hostname]).splitlines()[0]
    tokens = forward_line.split()
    assert tokens, (
        f"'getent hosts {hostname}' produced malformed output: {forward_line!r}"
    )

    ipv4 = tokens[0]
    assert IPV4_RE.match(ipv4), (
        f"Expected an IPv4 address as the first field when resolving {hostname!r}, "
        f"but got {ipv4!r}."
    )

    # 3. Reverse lookup: getent hosts <ipv4>
    reverse_line = _run(["getent", "hosts", ipv4]).splitlines()[0]
    rev_tokens = reverse_line.split()
    assert len(rev_tokens) >= 2, (
        f"Reverse lookup for {ipv4!r} did not return an FQDN: {reverse_line!r}"
    )

    reverse_fqdn = rev_tokens[1]
    assert reverse_fqdn, (
        f"PTR record for {ipv4!r} was empty in output: {reverse_line!r}"
    )