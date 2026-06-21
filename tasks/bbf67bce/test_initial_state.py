# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state
# before the student performs any actions for the “site backup”
# exercise.  It checks for the presence and correctness of the
# source project tree under /home/user/web_project as well as
# the existence (and emptiness) of /home/user/backups.
#
# NOTE: Per grading rules we purposely do *not* test for the
#       existence (or absence) of the final output file
#       /home/user/backups/site_backup.tar.gz.

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants describing the expected initial state.
# ---------------------------------------------------------------------------

HOME = Path("/home/user")

PROJECT_ROOT = HOME / "web_project"
BACKUP_DIR = HOME / "backups"

EXPECTED_DIRS = [
    PROJECT_ROOT,
    PROJECT_ROOT / "css",
    PROJECT_ROOT / "js",
    PROJECT_ROOT / "img",
    BACKUP_DIR,
]

EXPECTED_TEXT_FILES = {
    PROJECT_ROOT / "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Demo Site</title>
</head>
<body>
    <h1>Welcome</h1>
</body>
</html>
""",
    PROJECT_ROOT / "css" / "style.css": "body { font-family: Arial, sans-serif; }",
    PROJECT_ROOT / "js" / "app.js": "console.log('Hello world');",
}

EXPECTED_BINARY_FILES = {
    PROJECT_ROOT
    / "img"
    / "logo.png": (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\nIDATx\xdacd\xf8\xff\xff?"
        b"\x00\x05\xfe\x02\xfeA \x94\x07\x00\x00\x00\x00IEND\xaeB`\x82"
    )
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def assert_path_is_dir(path: Path) -> None:
    assert path.exists(), f"Expected directory {path} is missing."
    assert path.is_dir(), f"{path} exists but is not a directory."


def assert_path_is_file(path: Path) -> None:
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_expected_directories_exist():
    """All required directories must exist."""
    for directory in EXPECTED_DIRS:
        assert_path_is_dir(directory)


def test_backup_directory_is_empty():
    """The backup directory must exist and be empty at the start."""
    assert_path_is_dir(BACKUP_DIR)
    leftover_items = list(BACKUP_DIR.iterdir())
    assert (
        len(leftover_items) == 0
    ), f"{BACKUP_DIR} should be empty initially, but contains: {leftover_items}"


def test_expected_text_files_exist_with_correct_content():
    """Verify that all expected text files are present and contain the exact text (ignoring trailing newlines)."""
    for path, expected_content in EXPECTED_TEXT_FILES.items():
        assert_path_is_file(path)
        actual_content = path.read_text(encoding="utf-8")
        # Compare stripped to ignore trailing newlines/spaces at EOF.
        assert (
            actual_content.strip() == expected_content.strip()
        ), f"Contents of {path} do not match expected."


def test_expected_binary_files_exist_with_correct_content():
    """Verify that all expected binary files are present and match the expected byte sequence."""
    for path, expected_bytes in EXPECTED_BINARY_FILES.items():
        assert_path_is_file(path)
        actual_bytes = path.read_bytes()
        assert (
            actual_bytes == expected_bytes
        ), f"Binary contents of {path} do not match expected contents."