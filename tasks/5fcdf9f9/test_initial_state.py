# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# for the “asset list” exercise.  These tests must pass *before* the
# student writes any code or generates any output files.

import os
from pathlib import Path

SITE_ROOT = Path("/home/user/site")
STATIC_DIR = SITE_ROOT / "static"

# Mapping of expected text files to their exact byte content
EXPECTED_TEXT_FILES = {
    STATIC_DIR / "app.js": b'console.log("App main");\n',
    STATIC_DIR / "utils" / "helper.js": b'export function help() { return true; }\n',
    STATIC_DIR / "css" / "style.css": b'body { margin: 0; }\n',
}

# Expected binary files (content is unconstrained, but the files must exist and be non-empty)
EXPECTED_BINARY_FILES = [
    STATIC_DIR / "images" / "logo.png",
]


def _assert_is_file(path: Path):
    assert path.exists(), f"Expected file '{path}' is missing."
    assert path.is_file(), f"Path '{path}' exists but is not a regular file."


def test_static_directory_exists():
    assert STATIC_DIR.exists(), f"Directory '{STATIC_DIR}' is missing."
    assert STATIC_DIR.is_dir(), f"Path '{STATIC_DIR}' exists but is not a directory."


def test_expected_text_files_exist_with_exact_content():
    """
    Verify that all required text files exist **and** contain the exact
    bytes stipulated by the task description (including trailing newlines).
    """
    for path, expected_bytes in EXPECTED_TEXT_FILES.items():
        _assert_is_file(path)

        actual_bytes = path.read_bytes()
        assert (
            actual_bytes == expected_bytes
        ), (
            f"File '{path}' exists but its contents are incorrect.\n"
            f"Expected bytes: {expected_bytes!r}\n"
            f"Actual bytes:   {actual_bytes!r}"
        )


def test_expected_binary_files_exist_and_are_non_empty():
    """
    Verify that required binary files (e.g., PNGs) exist and are not empty.
    Content is otherwise unconstrained.
    """
    for path in EXPECTED_BINARY_FILES:
        _assert_is_file(path)
        size = path.stat().st_size
        assert size > 0, f"File '{path}' is empty; expected non-empty binary content."