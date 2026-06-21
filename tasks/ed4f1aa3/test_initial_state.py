# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student performs any action on the documentation-compression
# exercise described in the assignment.  These tests check that
#
# 1. The directory /home/user/projects/manual exists.
# 2. It contains exactly three markdown files: intro.md, install.md,
#    usage.md — nothing more, nothing less.
# 3. Each of the three files is present with the exact byte-for-byte
#    contents stated in the assignment (including a single trailing LF).
# 4. The cumulative byte size of the three files equals 84 bytes.
# 5. Neither /home/user/doc_compressed nor /home/user/doc_extracted
#    exists yet.
#
# Only the Python stdlib and pytest are used.

from pathlib import Path
import os
import stat
import pytest

HOME = Path("/home/user")
MANUAL_DIR = HOME / "projects" / "manual"
DOC_COMPRESSED_DIR = HOME / "doc_compressed"
DOC_EXTRACTED_DIR = HOME / "doc_extracted"

EXPECTED_FILES = {
    "intro.md": "## Intro\nA brief introduction.\n",
    "install.md": "## Install\nUse `make install`.\n",
    "usage.md": "## Usage\nRun `./app`.\n",
}

@pytest.fixture(scope="module")
def manual_dir_contents():
    """
    Return a mapping of filename -> bytes of each file found in
    /home/user/projects/manual. Raises useful assertion errors if the
    directory is missing.
    """
    if not MANUAL_DIR.exists():
        pytest.fail(f"Required directory {MANUAL_DIR} is missing.")
    if not MANUAL_DIR.is_dir():
        pytest.fail(f"{MANUAL_DIR} exists but is not a directory.")
    contents = {}
    for p in MANUAL_DIR.iterdir():
        if p.is_file():
            contents[p.name] = p.read_bytes()
    return contents

def test_manual_directory_exists():
    """The /home/user/projects/manual directory must exist and be a directory."""
    assert MANUAL_DIR.exists(), f"Directory {MANUAL_DIR} does not exist."
    assert MANUAL_DIR.is_dir(), f"Path {MANUAL_DIR} exists but is not a directory."

def test_expected_markdown_files_present(manual_dir_contents):
    """Exactly the three expected markdown files must be present."""
    present = set(manual_dir_contents.keys())
    expected = set(EXPECTED_FILES.keys())
    extra = present - expected
    missing = expected - present
    assert not missing, (
        f"Missing expected file(s) in {MANUAL_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected extra file(s) present in {MANUAL_DIR}: {', '.join(sorted(extra))}"
    )

def test_exact_file_contents(manual_dir_contents):
    """Each markdown file must contain the exact expected content."""
    for filename, expected_text in EXPECTED_FILES.items():
        actual_bytes = manual_dir_contents[filename]
        expected_bytes = expected_text.encode("utf-8")
        assert actual_bytes == expected_bytes, (
            f"Content mismatch in {MANUAL_DIR / filename}.\n"
            f"Expected (repr): {repr(expected_text)}\n"
            f"Actual   (repr): {repr(actual_bytes.decode('utf-8', errors='replace'))}"
        )

def test_individual_file_sizes(manual_dir_contents):
    """Verify each file's size in bytes (helps pinpoint size errors)."""
    expected_sizes = {
        "intro.md": 31,
        "install.md": 31,
        "usage.md": 22,
    }
    for filename, size in expected_sizes.items():
        actual_size = len(manual_dir_contents[filename])
        assert actual_size == size, (
            f"Size of {MANUAL_DIR / filename} is {actual_size} bytes, "
            f"expected {size} bytes."
        )

def test_total_bytes(manual_dir_contents):
    """Total size of all three files must be 84 bytes."""
    total = sum(len(b) for b in manual_dir_contents.values())
    assert total == 84, f"Total size of markdown files is {total} bytes; expected 84 bytes."

def _path_does_not_exist(path: Path):
    # Helper for better error messages if a path unexpectedly exists.
    assert not path.exists(), (
        f"Path {path} should NOT exist in the initial state, "
        f"but it is present (type: {'directory' if path.is_dir() else 'file'})."
    )

def test_no_doc_compressed_yet():
    """doc_compressed directory (and its contents) must not exist initially."""
    _path_does_not_exist(DOC_COMPRESSED_DIR)

def test_no_doc_extracted_yet():
    """doc_extracted directory (and its contents) must not exist initially."""
    _path_does_not_exist(DOC_EXTRACTED_DIR)