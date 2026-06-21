# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state before the student
starts working.

It asserts that:
1. /home/user/docs exists, is a directory, and is writable.
2. Exactly three Markdown files exist directly inside /home/user/docs:
   - faq.md
   - introduction.md
   - usage-guide.md
3. Each of those files is empty (0 bytes) and readable.

No checks are performed for the output artefact (/home/user/docs/checksums.txt)
because the student will create it later.
"""

import os
from pathlib import Path
import stat

DOCS_DIR = Path("/home/user/docs")
EXPECTED_MD_FILES = {
    "faq.md",
    "introduction.md",
    "usage-guide.md",
}

def _is_writable(path: Path) -> bool:
    """
    Return True if the current user has write permission to `path`.
    """
    return os.access(path, os.W_OK)

def test_docs_directory_exists_and_writable():
    assert DOCS_DIR.exists(), f"Required directory {DOCS_DIR} is missing."
    assert DOCS_DIR.is_dir(), f"{DOCS_DIR} exists but is not a directory."
    assert _is_writable(DOCS_DIR), f"{DOCS_DIR} is not writable by the current user."

def test_markdown_files_exist_and_are_empty():
    md_files_in_dir = {p.name for p in DOCS_DIR.iterdir() if p.is_file() and p.suffix == ".md"}

    # Check that the expected set matches exactly.
    missing = EXPECTED_MD_FILES - md_files_in_dir
    unexpected = md_files_in_dir - EXPECTED_MD_FILES

    assert not missing, (
        "The following required .md file(s) are missing from "
        f"{DOCS_DIR}: {', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        "Unexpected .md file(s) found in "
        f"{DOCS_DIR}: {', '.join(sorted(unexpected))}"
    )

    # All expected files exist; ensure each is empty and readable.
    for filename in EXPECTED_MD_FILES:
        file_path = DOCS_DIR / filename
        assert file_path.is_file(), f"{file_path} should be a regular file."
        assert os.access(file_path, os.R_OK), f"{file_path} is not readable."
        size = file_path.stat().st_size
        assert size == 0, f"{file_path} is expected to be empty (0 bytes) but is {size} bytes."