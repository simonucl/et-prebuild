# test_initial_state.py
"""
Pytest suite to verify the *initial* state of the operating system / filesystem
before the student carries out any actions for the “localhost resolution” task.

We purposefully assert that:
1. The directory “/home/user/dns_audit/” does **not** yet exist.
2. Consequently, the file “/home/user/dns_audit/localhost_resolution.log” must
   also **not** exist.

If either of these paths is already present, the exercise is starting from an
unexpected state and should be corrected before grading continues.
"""

from pathlib import Path
import os
import pytest

HOME = Path("/home/user")
DNS_AUDIT_DIR = HOME / "dns_audit"
RESOLUTION_LOG = DNS_AUDIT_DIR / "localhost_resolution.log"


def _pretty_path(p: Path) -> str:
    """
    Produce a human-friendly representation of a Path for error messages.
    """
    return os.fspath(p.resolve())


def test_dns_audit_directory_absent():
    """
    The directory /home/user/dns_audit/ should NOT exist at the beginning of
    the exercise.  If it already exists, there is a risk that leftover files
    from previous runs will interfere with grading.
    """
    assert not DNS_AUDIT_DIR.exists(), (
        f"Unexpected pre-existing directory found: {_pretty_path(DNS_AUDIT_DIR)}\n"
        "The directory must NOT be present before the student creates it."
    )


def test_localhost_resolution_log_absent():
    """
    The log file /home/user/dns_audit/localhost_resolution.log must NOT exist
    before the student creates it.  Starting with this file already present
    would defeat the purpose of the task.
    """
    assert not RESOLUTION_LOG.exists(), (
        f"Unexpected pre-existing file found: {_pretty_path(RESOLUTION_LOG)}\n"
        "The file must NOT exist before the student runs their solution."
    )