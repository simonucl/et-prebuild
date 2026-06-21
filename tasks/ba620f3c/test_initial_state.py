# test_initial_state.py
"""
Pytest suite that validates the **initial** filesystem state for the
'junior compliance analyst' task *before* the student performs any work.

What is verified:

1. Mandatory base paths and files exist.
2. The SSH configuration file is in its original (un-hardened) form.
3. Reference audit-log samples are present and byte-for-byte correct.
4. No artefacts that the student is supposed to create later
   (scripts/, logs/, report/, etc.) are present yet.

Only Python's stdlib and pytest are used.
"""

import os
from pathlib import Path

BASE_DIR = Path("/home/user/compliance")
CONFIGS_DIR = BASE_DIR / "configs"
REFERENCE_DIR = BASE_DIR / "reference"

SSHD_CONFIG = CONFIGS_DIR / "sshd_config"
PORTS_SAMPLE = REFERENCE_DIR / "ports_sample.log"
SERVICES_SAMPLE = REFERENCE_DIR / "services_sample.log"

# Paths that should *not* exist before the student acts
SCRIPTS_DIR = BASE_DIR / "scripts"
LOGS_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "report"
PORT_AUDIT_SH = SCRIPTS_DIR / "port_audit.sh"
SERVICE_AUDIT_SH = SCRIPTS_DIR / "service_audit.sh"
PORT_AUDIT_LOG = LOGS_DIR / "port_audit.log"
SERVICE_AUDIT_LOG = LOGS_DIR / "service_audit.log"
ACTION_LOG = LOGS_DIR / "action.log"
COMPLIANCE_REPORT = REPORT_DIR / "compliance_report.json"


def test_base_directories_exist():
    assert BASE_DIR.is_dir(), f"Required directory '{BASE_DIR}' is missing."
    assert CONFIGS_DIR.is_dir(), f"Required directory '{CONFIGS_DIR}' is missing."
    assert REFERENCE_DIR.is_dir(), f"Required directory '{REFERENCE_DIR}' is missing."


def test_sshd_config_exists_and_unhardened():
    assert SSHD_CONFIG.is_file(), f"File '{SSHD_CONFIG}' is missing."

    contents = SSHD_CONFIG.read_text().splitlines()
    # Look for exact, unmodified lines (whitespace sensitive)
    assert "PermitRootLogin yes" in contents, (
        "'PermitRootLogin yes' line is missing or has been altered. "
        "The SSH configuration must be unhardened initially."
    )
    assert "PasswordAuthentication yes" in contents, (
        "'PasswordAuthentication yes' line is missing or has been altered. "
        "The SSH configuration must be unhardened initially."
    )

    # Hardened strings must NOT be present yet
    assert "PermitRootLogin no" not in contents, (
        "Configuration already shows 'PermitRootLogin no'; "
        "the hardening step has been performed too early."
    )
    assert "PasswordAuthentication no" not in contents, (
        "Configuration already shows 'PasswordAuthentication no'; "
        "the hardening step has been performed too early."
    )


def test_reference_ports_sample_correct():
    expected = (
        "tcp        0      0 0.0.0.0:22            0.0.0.0:*               LISTEN\n"
        "tcp        0      0 127.0.0.1:631         0.0.0.0:*               LISTEN\n"
        "udp        0      0 0.0.0.0:68            0.0.0.0:*              \n"
    )
    assert PORTS_SAMPLE.is_file(), f"Reference file '{PORTS_SAMPLE}' is missing."
    actual = PORTS_SAMPLE.read_text()
    assert actual == expected, (
        f"'{PORTS_SAMPLE}' does not match the expected byte-for-byte content."
    )


def test_reference_services_sample_correct():
    expected = (
        "sshd\n"
        "cupsd\n"
        "dhclient\n"
        "systemd\n"
    )
    assert SERVICES_SAMPLE.is_file(), f"Reference file '{SERVICES_SAMPLE}' is missing."
    actual = SERVICES_SAMPLE.read_text()
    assert actual == expected, (
        f"'{SERVICES_SAMPLE}' does not match the expected byte-for-byte content."
    )


def test_student_output_artifacts_absent():
    """
    Ensure that no artefacts the student is supposed to create later
    are present **before** the task is attempted.
    """
    paths_that_must_not_exist = [
        SCRIPTS_DIR,
        LOGS_DIR,
        REPORT_DIR,
        PORT_AUDIT_SH,
        SERVICE_AUDIT_SH,
        PORT_AUDIT_LOG,
        SERVICE_AUDIT_LOG,
        ACTION_LOG,
        COMPLIANCE_REPORT,
    ]

    offending = [str(p) for p in paths_that_must_not_exist if p.exists()]
    assert not offending, (
        "The following path(s) already exist but should not be present "
        "before the student executes the task:\n" + "\n".join(offending)
    )