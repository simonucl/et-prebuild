# test_initial_state.py
"""
Pytest suite that validates the **initial** filesystem state before the
student rotates any credentials.

Checks performed:
1. /home/user/secrets directory exists.
2. /home/user/secrets/credentials.csv exists.
3. credentials.csv content is **byte-for-byte** exactly as specified
   (UTF-8, LF line endings).
4. No other files (regular files, dirs, symlinks, etc.) are present in
   /home/user/secrets.
"""

import os
from pathlib import Path

import pytest

SECRETS_DIR = Path("/home/user/secrets")
CREDENTIALS_CSV = SECRETS_DIR / "credentials.csv"

# Expected credentials.csv bytes (including final newline)
EXPECTED_CSV_BYTES = (
    b"app_name,username,password,last_rotated\n"
    b"billing-service,bill-user,B!llPass123,2022-12-01\n"
    b"auth-service,auth-user,Aut#2020,2023-04-15\n"
    b"reporting-service,rep-user,Rep0rt!,2022-11-20\n"
    b"legacy-api,legacy-user,L3gacyPwd,2022-01-10\n"
)


def test_secrets_directory_exists():
    assert SECRETS_DIR.is_dir(), (
        f"Required directory {SECRETS_DIR} is missing. "
        "Create it before proceeding."
    )


def test_credentials_csv_exists():
    assert CREDENTIALS_CSV.is_file(), (
        f"Required file {CREDENTIALS_CSV} is missing. "
        "Ensure the original credentials CSV is present."
    )


def test_credentials_csv_content_exact():
    actual_bytes = CREDENTIALS_CSV.read_bytes()
    assert (
        actual_bytes == EXPECTED_CSV_BYTES
    ), (
        f"{CREDENTIALS_CSV} content does not match the expected initial "
        "state. Do not modify the file before credential rotation."
    )


def test_no_other_files_in_secrets():
    """
    Ensure no extra artefacts are present yet. This prevents students from
    accidentally producing output files before the tests that expect them.
    """
    entries = [p for p in SECRETS_DIR.iterdir() if p.name not in {".", ".."}]
    unexpected = [p for p in entries if p != CREDENTIALS_CSV]
    assert not unexpected, (
        "Unexpected files/directories found in /home/user/secrets:\n"
        + "\n".join(str(p) for p in unexpected)
        + "\nRemove them before running the credential-rotation script."
    )