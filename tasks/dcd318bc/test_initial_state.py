# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
before the student’s solution is run.

It checks only the artefacts that are supposed to exist _before_ the student
acts, and never touches the output target (/home/user/reports/…).

Requirements verified:
1. /home/user/webpages/ directory exists and has at least user-read/execute
   permission.
2. /home/user/webpages/mobile_builds.html exists, is a regular file, is
   readable by the owner, and contains the exact four version strings that the
   task description specifies—in the correct order and with no extras.
"""

import os
import re
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   
# --------------------------------------------------------------------------- #

WEBPAGES_DIR = Path("/home/user/webpages")
HTML_FILE = WEBPAGES_DIR / "mobile_builds.html"

EXPECTED_VERSIONS = [
    "v2.3.1",
    "v2.3.0",
    "v2.2.5",
    "v2.2.4",
]

VERSION_REGEX = re.compile(r'<span\s+class="version">(?P<ver>v\d+\.\d+\.\d+)</span>')


# --------------------------------------------------------------------------- #
# Helpers                                                                     
# --------------------------------------------------------------------------- #
def _octal_mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o644) of a path."""
    return path.stat().st_mode & 0o777


# --------------------------------------------------------------------------- #
# Tests                                                                       
# --------------------------------------------------------------------------- #
def test_webpages_directory_exists_and_permissions():
    assert WEBPAGES_DIR.is_dir(), (
        f"Required directory {WEBPAGES_DIR} is missing."
    )

    mode = _octal_mode(WEBPAGES_DIR)
    # Expect at least user read & execute (0o500) so that files inside are reachable.
    assert mode & 0o500 == 0o500, (
        f"Directory {WEBPAGES_DIR} exists but lacks user read/execute permissions "
        f"(current mode: {oct(mode)})."
    )


def test_html_file_exists_is_file_and_permissions():
    assert HTML_FILE.exists(), f"Required file {HTML_FILE} is missing."
    assert HTML_FILE.is_file(), f"{HTML_FILE} exists but is not a regular file."

    mode = _octal_mode(HTML_FILE)
    # Expect at least user read (0o400)
    assert mode & 0o400 == 0o400, (
        f"File {HTML_FILE} exists but is not readable by the owner "
        f"(current mode: {oct(mode)})."
    )


def test_html_file_contains_expected_versions_only_and_in_order():
    html_text = HTML_FILE.read_text(encoding="utf-8")

    # Extract every <span class="version">…</span> occurrence
    found_versions = VERSION_REGEX.findall(html_text)

    # 1. Correct count
    assert len(found_versions) == len(
        EXPECTED_VERSIONS
    ), (
        f"{HTML_FILE} should contain exactly {len(EXPECTED_VERSIONS)} "
        f'version spans, but {len(found_versions)} were found: {found_versions!r}.'
    )

    # 2. Correct order & exact values
    assert found_versions == EXPECTED_VERSIONS, (
        f"Versions found in {HTML_FILE} are not in the expected order or "
        f"do not match exactly.\nExpected: {EXPECTED_VERSIONS}\nFound:    {found_versions}"
    )

    # 3. Ensure no other version-looking strings lurk elsewhere in the file
    all_version_like = re.findall(r"\bv\d+\.\d+\.\d+\b", html_text)
    assert all_version_like == EXPECTED_VERSIONS, (
        "The HTML file contains version-looking strings outside of the "
        '<span class="version"> tags. Full list found: '
        f"{all_version_like}"
    )