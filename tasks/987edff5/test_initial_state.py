# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state _before_ the
# student performs any actions for the “account-lockout policy” exercise.
#
# What we check:
#   1. /home/user/compliance/     … exists and is a directory.
#   2. /home/user/compliance/failed_logins.tsv
#        • exists and is a regular file
#        • its contents match the exact, pre-populated, tab-separated data
#          (including the final newline)
#
# What we deliberately do **NOT** check:
#   • /home/user/compliance/analysis/ and anything inside it
#     (these are output artefacts and must not be inspected at this stage).
#
# Only stdlib and pytest are used, in compliance with the project rules.

from pathlib import Path
import pytest

COMPLIANCE_DIR = Path("/home/user/compliance")
FAILED_LOGINS_FILE = COMPLIANCE_DIR / "failed_logins.tsv"

# The exact, sanctioned contents of the pre-existing audit file.
EXPECTED_FAILED_LOGINS_CONTENT = (
    "username\tip_address\ttimestamp\tattempts\n"
    "alice\t10.0.0.5\t2023-08-01T12:01:22Z\t3\n"
    "bob\t10.0.0.6\t2023-08-01T12:02:17Z\t7\n"
    "carol\t10.0.0.7\t2023-08-01T12:04:03Z\t5\n"
    "dave\t10.0.0.8\t2023-08-01T12:05:55Z\t10\n"
)


def test_compliance_directory_exists():
    """The /home/user/compliance directory must be present."""
    assert COMPLIANCE_DIR.is_dir(), (
        "Required directory '/home/user/compliance' is missing. "
        "The exercise expects this directory to be pre-populated."
    )


def test_failed_logins_file_exists_with_correct_content():
    """Validate presence and exact contents of failed_logins.tsv."""
    assert FAILED_LOGINS_FILE.is_file(), (
        "Expected file '/home/user/compliance/failed_logins.tsv' is missing."
    )

    actual_content = FAILED_LOGINS_FILE.read_text(encoding="utf-8")

    # Perform a strict comparison so any deviation (missing newline, bad tab,
    # wrong line order, etc.) results in a clear failure.
    assert actual_content == EXPECTED_FAILED_LOGINS_CONTENT, (
        "The contents of '/home/user/compliance/failed_logins.tsv' do not match "
        "the expected pre-populated data. Ensure the file contains exactly the "
        "specified header and four data lines with TAB separators, and that "
        "there is a single trailing newline."
    )