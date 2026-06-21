# test_initial_state.py
#
# This pytest suite validates the machine’s initial state **before**
# students attempt the credential-rotation task.  It checks only the
# pre-existing resources described in the assignment and explicitly
# avoids touching any output paths (e.g., /home/user/security/).
#
# Tested items:
#   1. /home/user/web/credentials.html exists and is a regular file.
#   2. The file’s single-line content matches the expected HTML and
#      contains the username “new_admin”.

from pathlib import Path
import re
import pytest


CREDENTIALS_PATH = Path("/home/user/web/credentials.html")
EXPECTED_HTML_EXACT = "<div id=\"current-user\">new_admin</div>"
HTML_REGEX = re.compile(r'^<div id="current-user">\s*new_admin\s*</div>\s*$')


def test_credentials_file_exists():
    """Ensure the credentials.html file is present and is a regular file."""
    assert CREDENTIALS_PATH.exists(), (
        f"Missing required file: {CREDENTIALS_PATH}. "
        "The rotation job is supposed to write this HTML snippet."
    )
    assert CREDENTIALS_PATH.is_file(), (
        f"{CREDENTIALS_PATH} exists but is not a regular file."
    )


def test_credentials_file_content():
    """
    Confirm the credentials.html file contains exactly the expected single line
    with the <div id="current-user">new_admin</div> snippet.
    """
    content = CREDENTIALS_PATH.read_text(encoding="utf-8").strip()

    # First, a forgiving regex match (allows stray whitespace).
    assert HTML_REGEX.match(content), (
        "The contents of /home/user/web/credentials.html do not match the "
        "expected format. Expected something like:\n"
        '    <div id="current-user">new_admin</div>'
    )

    # Second, enforce the *exact* string (no hidden characters) so that
    # downstream extraction commands behave predictably.
    assert content == EXPECTED_HTML_EXACT, (
        "The credentials file should contain exactly this one line:\n"
        f"    {EXPECTED_HTML_EXACT}\n"
        f"Found instead:\n"
        f"    {content}"
    )