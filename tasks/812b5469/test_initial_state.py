# test_initial_state.py
"""
Pytest suite to validate the *initial* operating-system / filesystem state
BEFORE the student’s solution is run.

Expected initial conditions (summarised):
1. Directory  : /home/user/portal/          → exists, contains ONLY rotation.html
2. File       : /home/user/portal/rotation.html
               → contains exactly one <code id="api-token">SECURETOKEN12345</code>
3. Directory  : /home/user/credentials/     → exists, is writable, currently EMPTY
No other files or directories are expected at this stage.
"""

import os
import re
from pathlib import Path

# --- Constants --------------------------------------------------------------

PORTAL_DIR = Path("/home/user/portal")
ROTATION_FILE = PORTAL_DIR / "rotation.html"
CREDENTIALS_DIR = Path("/home/user/credentials")
EXPECTED_TOKEN = "SECURETOKEN12345"
EXPECTED_CODE_TAG = f'<code id="api-token">{EXPECTED_TOKEN}</code>'


# --- Helper -----------------------------------------------------------------

def list_dir_entries(path: Path):
    """Return a list of (name, is_dir) tuples for every entry in *path*."""
    return sorted([(p.name, p.is_dir()) for p in path.iterdir()])


# --- Tests ------------------------------------------------------------------

def test_portal_directory_exists_and_has_only_rotation_html():
    assert PORTAL_DIR.exists(), f"Directory {PORTAL_DIR} is missing."
    assert PORTAL_DIR.is_dir(), f"{PORTAL_DIR} exists but is not a directory."

    contents = list(PORTAL_DIR.iterdir())
    assert contents, f"{PORTAL_DIR} is empty; expected rotation.html."
    assert len(contents) == 1 and contents[0].name == "rotation.html", (
        f"{PORTAL_DIR} should contain ONLY 'rotation.html'. "
        f"Found: {[p.name for p in contents]}"
    )


def test_rotation_html_contains_exact_code_tag_once():
    assert ROTATION_FILE.exists(), f"File {ROTATION_FILE} is missing."
    assert ROTATION_FILE.is_file(), f"{ROTATION_FILE} exists but is not a file."

    text = ROTATION_FILE.read_text(encoding="utf-8")

    # 1) Exact code tag present exactly once
    occurrences = text.count(EXPECTED_CODE_TAG)
    assert occurrences == 1, (
        f"Expected exactly one occurrence of '{EXPECTED_CODE_TAG}' in {ROTATION_FILE}, "
        f"found {occurrences}."
    )

    # 2) No other <code> tags are present
    all_code_tags = re.findall(r"<code[^>]*>.*?</code>", text, flags=re.DOTALL)
    assert len(all_code_tags) == 1, (
        f"Only one <code> tag should be present in {ROTATION_FILE}. "
        f"Found {len(all_code_tags)} tags: {all_code_tags}"
    )


def test_credentials_directory_exists_is_writable_and_empty():
    assert CREDENTIALS_DIR.exists(), f"Directory {CREDENTIALS_DIR} is missing."
    assert CREDENTIALS_DIR.is_dir(), f"{CREDENTIALS_DIR} exists but is not a directory."
    assert os.access(CREDENTIALS_DIR, os.W_OK), (
        f"Directory {CREDENTIALS_DIR} is not writable by the current user."
    )

    entries = list_dir_entries(CREDENTIALS_DIR)
    assert entries == [], (
        f"{CREDENTIALS_DIR} should be EMPTY at the start. "
        f"Found entries: {entries}"
    )