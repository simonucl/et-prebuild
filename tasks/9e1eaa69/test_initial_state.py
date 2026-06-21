# test_initial_state.py
#
# Pytest suite that validates the machine *before* the student runs
# any commands for the “openssl audit-trail” exercise.
#
# Expectations for the pristine starting state:
#   • /home/user/compliance          MUST NOT exist yet.
#   • /home/user/compliance/openssl_audit.log MUST NOT exist yet.
#   • OpenSSL *is* installed and queryable with dpkg/apt so that the
#     student can retrieve the installed‐ and candidate-version strings.
#
# Only Python stdlib and pytest are used.

import subprocess
from pathlib import Path
import re
import pytest


COMPLIANCE_DIR = Path("/home/user/compliance")
AUDIT_FILE = COMPLIANCE_DIR / "openssl_audit.log"


def _run(cmd):
    """
    Helper to run a shell command and return stripped stdout.

    Raises AssertionError with useful context if the command fails.
    """
    proc = subprocess.run(
        cmd, shell=True, check=False, text=True, capture_output=True
    )
    assert proc.returncode == 0, (
        f"Command failed ({proc.returncode}): {cmd}\n"
        f"stdout: {proc.stdout}\nstderr: {proc.stderr}"
    )
    return proc.stdout.strip()


def test_compliance_directory_absent():
    """The /home/user/compliance directory must NOT exist yet."""
    assert not COMPLIANCE_DIR.exists(), (
        "The directory /home/user/compliance already exists. "
        "The environment must start clean so the student can create it."
    )


def test_compliance_log_absent():
    """The openssl_audit.log file must NOT exist yet."""
    assert not AUDIT_FILE.exists(), (
        "The file /home/user/compliance/openssl_audit.log already exists. "
        "The environment must start clean so the student can create it."
    )


def test_openssl_installed_and_queryable():
    """
    dpkg-query must be able to return a non-empty version string for openssl.
    This guarantees the student can collect the INSTALLED= value later on.
    """
    version = _run("dpkg-query -W -f='${Version}' openssl")
    assert version, (
        "dpkg-query returned an empty version string for OpenSSL; "
        "OpenSSL must be installed for the exercise to succeed."
    )
    # Basic semantic-version looking pattern: digits & dots plus optional dash-suffix.
    assert re.fullmatch(r"[0-9][0-9A-Za-z.+:~-]*", version), (
        f"dpkg-query returned an unexpected version string: {version!r}"
    )


def test_openssl_candidate_queryable():
    """
    apt-cache must expose a Candidate: line for openssl so the student
    can capture the CANDIDATE= value.
    """
    candidate = _run("apt-cache policy openssl | awk '/Candidate:/ {print $2}'")
    assert candidate, (
        "Unable to obtain a candidate version for OpenSSL via apt-cache policy. "
        "The package metadata must be available."
    )
    # Same loose pattern as for installed version.
    assert re.fullmatch(r"[0-9][0-9A-Za-z.+:~-]*", candidate), (
        f"apt-cache returned an unexpected candidate string: {candidate!r}"
    )