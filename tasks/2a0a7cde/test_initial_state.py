# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# for the “ISO-8859-1 to UTF-8 conversion” exercise.  These tests
# must all pass *before* the student runs their conversion script.
#
# Requirements being checked:
#   • The /home/user/project/docs directory exists.
#   • It contains exactly three text files directly inside it:
#         changelog.txt
#         license.txt
#         readme.txt
#   • Each file is currently encoded in ISO-8859-1 and NOT in UTF-8.
#   • No other “.txt” files are present in that directory (or its
#     sub-directories).
#   • /home/user/project/encoding_conversion.log does NOT exist yet.
#
# Only Python stdlib + pytest are used.

import os
from pathlib import Path
import pytest
import codecs

DOCS_DIR = Path("/home/user/project/docs")
LOG_FILE = Path("/home/user/project/encoding_conversion.log")

EXPECTED_FILES = {
    "changelog.txt",
    "license.txt",
    "readme.txt",
}


def _list_txt_files(directory: Path, recursive: bool = False):
    """
    Helper that returns a set of pathlib.Path objects for .txt files.
    If recursive is False, only files directly inside `directory`
    are listed.  If recursive is True, the whole tree is walked.
    """
    if recursive:
        return {p for p in directory.rglob("*.txt") if p.is_file()}
    else:
        return {p for p in directory.glob("*.txt") if p.is_file()}


def test_docs_directory_exists():
    assert DOCS_DIR.exists(), (
        f"Expected directory {DOCS_DIR} to exist, but it is missing."
    )
    assert DOCS_DIR.is_dir(), (
        f"{DOCS_DIR} exists but is not a directory."
    )


def test_expected_txt_files_present_and_no_extras():
    direct_txt_files = _list_txt_files(DOCS_DIR, recursive=False)
    direct_names = {p.name for p in direct_txt_files}

    # Presence checks
    missing = EXPECTED_FILES - direct_names
    assert not missing, (
        "The following required .txt files are missing in "
        f"{DOCS_DIR}: {', '.join(sorted(missing))}"
    )

    # Exclusivity check (no extras directly inside docs)
    extras = direct_names - EXPECTED_FILES
    assert not extras, (
        "Unexpected .txt files found directly inside "
        f"{DOCS_DIR}: {', '.join(sorted(extras))}"
    )

    # No extra .txt files anywhere in sub-directories
    recursive_txt_files = _list_txt_files(DOCS_DIR, recursive=True)
    recursive_extras = {p.name for p in recursive_txt_files} - EXPECTED_FILES
    assert not recursive_extras, (
        "Unexpected .txt files found in sub-directories of "
        f"{DOCS_DIR}: {', '.join(sorted(recursive_extras))}"
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES))
def test_files_are_iso8859_not_utf8(filename):
    """Each file must currently be ISO-8859-1 and NOT UTF-8."""
    file_path = DOCS_DIR / filename
    assert file_path.exists(), f"Required file {file_path} is missing."

    raw_bytes = file_path.read_bytes()

    # 1. Must decode cleanly as ISO-8859-1
    try:
        codecs.decode(raw_bytes, "iso-8859-1")
    except Exception as exc:
        pytest.fail(
            f"{file_path} should be ISO-8859-1 but failed to decode as such: {exc}"
        )

    # 2. Must *not* decode as UTF-8 (should raise UnicodeDecodeError)
    with pytest.raises(UnicodeDecodeError):
        codecs.decode(raw_bytes, "utf-8")


def test_log_file_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should not exist before the conversion is performed."
    )