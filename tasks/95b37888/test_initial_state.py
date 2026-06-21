# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state **before** the student starts working on the task.
#
# IMPORTANT:  These tests must all pass *before* the student solution is
# executed.  They verify that the provided environment really matches the
# description in the exercise text.

import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
SYSTEM_LOG = LOG_DIR / "system.log"
SIG_FILE = LOG_DIR / "system.log.sig"
README = LOG_DIR / "README.txt"
VERIFY_REPORT = LOG_DIR / "verify_report.txt"

EXPECTED_LOG_LINES = [
    "2023-05-11 23:59:57 GET /index.html 200 123",
    "2023-05-11 23:59:58 GET /style.css 200 12",
    "2023-05-11 23:59:58 GET /script.js 200 45",
    "2023-05-11 23:59:59 GET /favicon.ico 200 2",
    "2023-05-12 00:00:01 GET /contact.html 404 0",
    "2023-05-12 00:00:03 POST /api/login 302 0",
    "2023-05-12 00:00:04 GET /dashboard 200 98",
]

FINGERPRINT_NO_SPACES = "9F2B8F5D8933E4E0A97E3C9EA0F2C894D9E0D123"


def _assert_mode(path: Path, expected_mode: int):
    """Assert a file/dir has the expected permission bits (lowest 3 octal digits)."""
    st_mode = path.stat().st_mode
    actual = stat.S_IMODE(st_mode)
    assert (
        actual == expected_mode
    ), f"{path}: expected permissions {oct(expected_mode)}, found {oct(actual)}"


def test_directory_structure_and_permissions():
    # Directory must exist
    assert LOG_DIR.is_dir(), f"Directory {LOG_DIR} is missing."
    # Permissions 0755
    _assert_mode(LOG_DIR, 0o755)

    # Critical files must exist
    for p in (SYSTEM_LOG, SIG_FILE, README):
        assert p.is_file(), f"Expected file {p} does not exist."

    # Report must **not** exist yet
    assert not VERIFY_REPORT.exists(), (
        f"{VERIFY_REPORT} should NOT exist before the student solution runs."
    )


def test_system_log_contents_and_permissions():
    _assert_mode(SYSTEM_LOG, 0o644)

    # Read file – ensure UTF-8 and exact content (strip final newline for comparison)
    data = SYSTEM_LOG.read_text(encoding="utf-8").splitlines()
    assert (
        data == EXPECTED_LOG_LINES
    ), "system.log does not contain the expected 7 log lines."


def test_signature_file_permissions_and_non_empty():
    # Only check that the signature file is present, readable and not empty
    _assert_mode(SIG_FILE, 0o644)
    size = SIG_FILE.stat().st_size
    assert size > 0, f"Signature file {SIG_FILE} is empty."


def _run_gpg(cmd_args):
    """Run a gpg command and return (rc, stdout, stderr)."""
    try:
        proc = subprocess.run(
            ["gpg", "--batch", "--no-tty", *cmd_args],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:  # pragma: no cover
        pytest.fail("gpg executable not found on the system – cannot continue tests.")
    return proc.returncode, proc.stdout, proc.stderr


def test_public_key_present_in_keyring():
    rc, out, err = _run_gpg(["--list-keys", "--with-colons"])
    assert rc == 0, f"gpg --list-keys failed: {err or out}"

    fingerprints = [
        line.split(":")[9]  # 10th field holds the fingerprint
        for line in out.splitlines()
        if line.startswith("fpr:")
    ]
    assert (
        FINGERPRINT_NO_SPACES in fingerprints
    ), f"Expected public key fingerprint {FINGERPRINT_NO_SPACES} not found in keyring."


def test_signature_is_valid():
    # Verify the detached signature – capture the machine-readable status lines
    rc, status_out, _ = _run_gpg(
        ["--status-fd", "1", "--verify", str(SIG_FILE), str(SYSTEM_LOG)]
    )
    assert rc == 0, "Detached signature verification failed."

    status_lines = status_out.splitlines()
    has_goodsig = any(line.startswith("[GNUPG:] GOODSIG") for line in status_lines)
    has_validsig = any(line.startswith("[GNUPG:] VALIDSIG") for line in status_lines)

    assert has_goodsig, "Expected [GNUPG:] GOODSIG line not found in gpg status output."
    assert has_validsig, "Expected [GNUPG:] VALIDSIG line not found in gpg status output."


def test_report_still_absent_after_tests():
    # The verification above must NOT create the report file that the student is supposed to make.
    assert (
        not VERIFY_REPORT.exists()
    ), f"{VERIFY_REPORT} should not exist yet; it must be created by the student."