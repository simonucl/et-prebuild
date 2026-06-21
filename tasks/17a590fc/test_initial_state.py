# test_initial_state.py
"""
Pytest suite validating the initial filesystem state *before* the student
runs any commands.  It confirms that the SSH hardening profile exists at the
expected absolute path and that its contents are exactly as prescribed.

Do NOT add tests for any output artefacts that the student is supposed to
create later.
"""

import os
from pathlib import Path

INI_PATH = Path("/home/user/sysconfigs/ssh_hardening.ini")

# Exact expected contents of the INI file, including all new-lines.
EXPECTED_INI_CONTENT = (
    "[SSH]\n"
    "# AllowedCiphers is a comma-separated list.  It may contain extra spaces.\n"
    "AllowedCiphers = aes256-ctr , aes192-ctr,aes128-ctr , chacha20-poly1305\n"
    "\n"
    "[RandomUnusedSection]\n"
    "Foo = bar\n"
)


def test_ini_file_exists():
    """
    The hardening profile must already exist at the given absolute path.
    """
    assert INI_PATH.is_file(), (
        f"Expected INI file not found: {INI_PATH}\n"
        "Make sure the file is present before running the task."
    )


def test_ini_file_content_exact_match():
    """
    The INI file must match exactly, character for character, including
    whitespace and newlines.  Any deviation means the starting state has
    been altered.
    """
    content = INI_PATH.read_text(encoding="utf-8")
    assert content == EXPECTED_INI_CONTENT, (
        "INI file contents do not match the expected initial state.\n\n"
        "----- Expected -----\n"
        f"{EXPECTED_INI_CONTENT!r}\n"
        "----- Found -----\n"
        f"{content!r}\n"
        "-------------------\n"
        "Verify the file has not been modified."
    )