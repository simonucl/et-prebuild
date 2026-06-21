# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
*before* the student performs any action for the “backup-integrity” exercise.

The checks make sure that:
1. The /home/user/backup directory exists.
2. The source file /home/user/backup/report.tsv exists.
3. /home/user/backup/verification.txt does NOT yet exist.
4. The content of report.tsv is EXACTLY the tab-separated block stated in the
   task description (byte-for-byte, including the final newline).

If any assertion fails, the error message pinpoints what is missing or wrong.
"""

from pathlib import Path
import pytest

HOME = Path("/home/user")
BACKUP_DIR = HOME / "backup"
REPORT_TSV = BACKUP_DIR / "report.tsv"
VERIFICATION_TXT = BACKUP_DIR / "verification.txt"


@pytest.fixture(scope="module")
def expected_report_bytes() -> bytes:
    """
    Returns the expected byte sequence for /home/user/backup/report.tsv exactly
    as described in the task (LF line endings, tab separators, final newline).
    """
    expected_lines = [
        b"id\tfile\tsha256\tstatus\n",
        b"1001\tconfig.tar.gz\t5d41402abc4b2a76b9719d911017c592\tsuccess\n",
        b"1002\tdb.sql\t"
        b"da4b9237bacccdf19c0760cab7aec4a8359010b0\tsuccess\n",
        b"1003\tlogs.zip\t"
        b"77de68daecd823babbb58edb1c8e14d7106e83bb\tfailed\n",
        b"1004\tpictures.tar\t"
        b"1b6453892473a467d07372d45eb05abc2031647a\tsuccess\n",
    ]
    return b"".join(expected_lines)


def test_backup_directory_exists():
    assert BACKUP_DIR.is_dir(), (
        f"Required directory {BACKUP_DIR} is missing."
    )


def test_report_tsv_exists():
    assert REPORT_TSV.is_file(), (
        f"Required source file {REPORT_TSV} does not exist."
    )


def test_verification_txt_not_present_initially():
    assert not VERIFICATION_TXT.exists(), (
        f"{VERIFICATION_TXT} should NOT exist before the student runs their "
        "command, but it is already present."
    )


def test_report_tsv_content_exact(expected_report_bytes):
    actual = REPORT_TSV.read_bytes()
    assert actual == expected_report_bytes, (
        "The content of /home/user/backup/report.tsv does not match the "
        "expected initial dataset.\n\n"
        "Expected (repr):\n"
        f"{repr(expected_report_bytes)}\n\n"
        "Actual (repr):\n"
        f"{repr(actual)}"
    )