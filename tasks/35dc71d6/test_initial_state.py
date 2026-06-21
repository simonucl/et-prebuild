# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system state
# before the student begins work on the “compromised crontab” exercise.
#
# It checks that:
#   • /home/user/forensics/compromised.cron exists, is a regular file,
#     has mode 0644, and contains exactly the three expected cron lines.
#   • /home/user/forensics/cron_audit.log is **not** present yet
#     (the student must create it later).
#
# NO OTHER FILES ARE TO BE VERIFIED HERE.
#
# Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path
import pytest


HOME = Path("/home/user")
FORENSICS_DIR = HOME / "forensics"
COMPROMISED_CRON = FORENSICS_DIR / "compromised.cron"
CRON_AUDIT_LOG = FORENSICS_DIR / "cron_audit.log"

EXPECTED_CRON_CONTENT = (
    "*/5 * * * * /home/user/scripts/backup.sh\n"
    "0 3 * * * /home/user/scripts/cleanup.sh\n"
    "@reboot /home/user/scripts/bitcoin_miner.sh\n"
)


@pytest.fixture(scope="module")
def compromised_cron_path() -> Path:
    """Return the Path object for the compromised cron file."""
    return COMPROMISED_CRON


def test_forensics_directory_exists():
    assert FORENSICS_DIR.is_dir(), (
        f"Required directory '{FORENSICS_DIR}' is missing. "
        "It must exist before the task starts."
    )


def test_compromised_cron_file_exists(compromised_cron_path: Path):
    assert compromised_cron_path.exists(), (
        f"Expected file '{compromised_cron_path}' is missing."
    )
    assert compromised_cron_path.is_file(), (
        f"'{compromised_cron_path}' exists but is not a regular file."
    )


def test_compromised_cron_file_mode(compromised_cron_path: Path):
    file_mode = stat.S_IMODE(compromised_cron_path.stat().st_mode)
    expected_mode = 0o644
    assert file_mode == expected_mode, (
        f"File '{compromised_cron_path}' should have mode "
        f"{oct(expected_mode)} but has {oct(file_mode)}."
    )


def test_compromised_cron_file_content(compromised_cron_path: Path):
    actual_content = compromised_cron_path.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_CRON_CONTENT, (
        f"Contents of '{compromised_cron_path}' do not match the expected "
        "three cron lines.\n\n"
        "Expected:\n"
        f"{EXPECTED_CRON_CONTENT!r}\n\n"
        "Actual:\n"
        f"{actual_content!r}"
    )


def test_cron_audit_log_not_present_yet():
    assert not CRON_AUDIT_LOG.exists(), (
        f"'{CRON_AUDIT_LOG}' should NOT exist before the student creates it."
    )