# test_initial_state.py
#
# Pytest suite that verifies the machine’s initial state BEFORE the student
# performs any action.  It checks:
#   1. Presence and exact content of /home/user/web/targets.html
#   2. Existence and permissions of the three target files
#   3. Absence of /home/user/audit at the outset
#
# The tests purposefully fail with clear, descriptive messages if anything is
# missing or incorrectly configured.
#
# Only Python’s standard library and pytest are used.

import os
import re
import stat
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")
WEB_DIR = HOME / "web"
TARGETS_HTML = WEB_DIR / "targets.html"

TEST_DATA_DIR = HOME / "test_data"
EXPECTED_FILES = [
    TEST_DATA_DIR / "file_public.txt",
    TEST_DATA_DIR / "file_secure.txt",
    TEST_DATA_DIR / "exec.sh",
]
EXPECTED_PERMS = {
    EXPECTED_FILES[0]: 0o644,
    EXPECTED_FILES[1]: 0o750,
    EXPECTED_FILES[2]: 0o755,
}

AUDIT_DIR = HOME / "audit"

# Exact HTML document we expect to find (byte-for-byte, including newlines)
EXPECTED_HTML_DOC = """<!DOCTYPE html>
<html>
  <head><title>Permission Targets</title></head>
  <body>
    <h1>Files to Audit</h1>
    <ul>
      <li>/home/user/test_data/file_public.txt</li>
      <li>/home/user/test_data/file_secure.txt</li>
      <li>/home/user/test_data/exec.sh</li>
    </ul>
  </body>
</html>
"""

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def read_file(path: Path) -> str:
    """Read a text file, raising an informative AssertionError if it fails."""
    assert path.exists(), f"Expected file {path} to exist, but it does not."
    assert path.is_file(), f"Expected {path} to be a regular file."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pylint: disable=broad-except
        pytest.fail(f"Could not read {path}: {exc}")


def octal_permissions(path: Path) -> int:
    """Return the permission bits of *path* as an int, e.g. 0o644."""
    st_mode = path.stat().st_mode
    return stat.S_IMODE(st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_web_directory_and_file_exist():
    assert WEB_DIR.exists(), f"Directory {WEB_DIR} is missing."
    assert WEB_DIR.is_dir(), f"{WEB_DIR} is not a directory."
    assert TARGETS_HTML.exists(), f"HTML file {TARGETS_HTML} is missing."
    assert TARGETS_HTML.is_file(), f"{TARGETS_HTML} is not a regular file."


def test_targets_html_content_is_exact():
    actual_content = read_file(TARGETS_HTML)
    assert (
        actual_content == EXPECTED_HTML_DOC
    ), (
        "Content of targets.html does not match the expected document.\n"
        "----- Expected -----\n"
        f"{EXPECTED_HTML_DOC!r}\n"
        "------ Actual ------\n"
        f"{actual_content!r}\n"
        "Ensure no leading/trailing spaces or differing newlines exist."
    )


def test_targets_html_contains_correct_li_paths():
    """Parse <li>…</li> entries and verify paths & order."""
    html = read_file(TARGETS_HTML)
    found_paths = re.findall(r"<li>([^<]+)</li>", html)
    expected_paths = [str(p) for p in EXPECTED_FILES]
    assert (
        found_paths == expected_paths
    ), (
        "The <li> elements inside targets.html are incorrect.\n"
        f"Expected: {expected_paths}\n"
        f"Found:    {found_paths}"
    )


def test_test_data_directory_and_files_exist():
    assert TEST_DATA_DIR.exists(), f"Directory {TEST_DATA_DIR} is missing."
    assert TEST_DATA_DIR.is_dir(), f"{TEST_DATA_DIR} is not a directory."

    # Check for presence AND absence (no surprise files)
    present_files = sorted(TEST_DATA_DIR.iterdir())
    expected_files_sorted = sorted(EXPECTED_FILES)
    assert (
        present_files == expected_files_sorted
    ), (
        f"{TEST_DATA_DIR} should contain exactly the files: "
        f"{[p.name for p in expected_files_sorted]}, "
        f"but it currently contains: {[p.name for p in present_files]}"
    )

    # Individual existence checks for clarity
    for path in EXPECTED_FILES:
        assert path.exists(), f"Expected file {path} is missing."
        assert path.is_file(), f"{path} exists but is not a regular file."


def test_permissions_of_target_files():
    for path, expected_perm in EXPECTED_PERMS.items():
        actual_perm = octal_permissions(path)
        assert (
            actual_perm == expected_perm
        ), (
            f"File {path} has permissions {oct(actual_perm)}, "
            f"expected {oct(expected_perm)}."
        )


def test_audit_directory_absent():
    assert not AUDIT_DIR.exists(), (
        f"Directory {AUDIT_DIR} should NOT exist before the student starts, "
        "but it does."
    )