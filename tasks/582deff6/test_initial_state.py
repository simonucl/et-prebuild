# test_initial_state.py
#
# Pytest suite that verifies the **initial** operating-system / filesystem
# state *before* the student creates cert_report.log.
#
# What we check:
#   1. /home/user/diagnostics exists and is user-writable.
#   2. /home/user/diagnostics/certs exists.
#   3. The two expected certificate files are present:
#        • /home/user/diagnostics/certs/webapp.crt
#        • /home/user/diagnostics/certs/db.crt
#   4. Each certificate file contains exactly one line that starts with
#      “NotAfter=” and that line matches the timestamp specified in the
#      task’s ground-truth description.
#
# We deliberately do NOT look for /home/user/diagnostics/cert_report.log or
# any other output artefact—those belong to the student’s solution phase.

import os
import re
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
DIAG_DIR = HOME / "diagnostics"
CERTS_DIR = DIAG_DIR / "certs"

CERT_EXPECTATIONS = {
    CERTS_DIR / "db.crt": "2024-12-31T23:59:59Z",
    CERTS_DIR / "webapp.crt": "2026-06-11T12:00:00Z",
}

NOT_AFTER_RE = re.compile(r"^NotAfter=([0-9]{4}-[0-9]{2}-[0-9]{2}T"
                          r"[0-9]{2}:[0-9]{2}:[0-9]{2}Z)$")


def test_diagnostics_dir_exists_and_writable():
    """/home/user/diagnostics must exist and be writable by the current user."""
    assert DIAG_DIR.exists(), f"Directory {DIAG_DIR} is missing."
    assert DIAG_DIR.is_dir(), f"{DIAG_DIR} exists but is not a directory."

    # The path must be writable.  os.access uses the real UID/GID.
    assert os.access(DIAG_DIR, os.W_OK), (
        f"Directory {DIAG_DIR} is not writable by the current user."
    )

    # Basic sanity: owner permissions should include write.
    mode = DIAG_DIR.stat().st_mode
    assert mode & stat.S_IWUSR, (
        f"Directory {DIAG_DIR} should have owner-write permissions (mode {oct(mode)})."
    )


def test_certs_dir_exists():
    """/home/user/diagnostics/certs must exist."""
    assert CERTS_DIR.exists(), f"Directory {CERTS_DIR} is missing."
    assert CERTS_DIR.is_dir(), f"{CERTS_DIR} exists but is not a directory."


@pytest.mark.parametrize("cert_path, expected_timestamp", CERT_EXPECTATIONS.items())
def test_certificate_file_exists(cert_path: Path, expected_timestamp: str):
    """Each expected certificate file must be present."""
    assert cert_path.exists(), f"Certificate file {cert_path} is missing."
    assert cert_path.is_file(), f"{cert_path} exists but is not a regular file."
    # File should be non-empty.
    assert cert_path.stat().st_size > 0, f"Certificate file {cert_path} is empty."


@pytest.mark.parametrize("cert_path, expected_timestamp", CERT_EXPECTATIONS.items())
def test_not_after_line(cert_path: Path, expected_timestamp: str):
    """
    Each certificate file must contain exactly one 'NotAfter=' line whose
    timestamp matches the ground-truth value.
    """
    with cert_path.open(encoding="utf-8") as fp:
        lines = [ln.rstrip("\n") for ln in fp]

    not_after_lines = [ln for ln in lines if ln.startswith("NotAfter=")]

    assert not_after_lines, (
        f"{cert_path} does not contain any line starting with 'NotAfter='."
    )
    assert len(not_after_lines) == 1, (
        f"{cert_path} contains multiple 'NotAfter=' lines: {not_after_lines}"
    )

    line = not_after_lines[0]
    m = NOT_AFTER_RE.match(line)
    assert m, (
        f"The 'NotAfter=' line in {cert_path} is malformed: {line!r}"
    )

    actual_timestamp = m.group(1)
    assert actual_timestamp == expected_timestamp, (
        f"Timestamp mismatch in {cert_path}. "
        f"Expected {expected_timestamp!r}, found {actual_timestamp!r}."
    )