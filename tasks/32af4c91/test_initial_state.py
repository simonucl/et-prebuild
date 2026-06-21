# test_initial_state.py
#
# Pytest suite that validates the initial, pre-conversion state of the
# filesystem for the “mobile_pipeline” i18n transcoding exercise.
#
# IMPORTANT:
#   * These tests purposefully avoid touching **any** of the artefacts that
#     the student is expected to create later (i18n_utf8/ directory,
#     encoding_conversion.log, etc.).  We only look at what must already be
#     present when the session starts.
#
#   * All paths are absolute and refer to /home/user/…  as required.
#
#   * Only the Python standard library + pytest are used.
#
#   * Failure messages are explicit so that a student instantly knows what
#     prerequisite is missing.

import os
import stat
import re
import pytest
from pathlib import Path

PROJECT_ROOT = Path("/home/user/mobile_pipeline")
SOURCE_DIR = PROJECT_ROOT / "i18n_source"

PROPERTIES_FILES = {
    "en_US.properties",
    "es_ES.properties",
    "jp_JP.properties",
}

README_FILE = PROJECT_ROOT / "README.txt"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _perm(path: Path) -> int:
    """
    Return the permission bits (e.g. 0o755) for the given file/dir.
    """
    return stat.S_IMODE(path.stat().st_mode)


def _has_only_crlf(data: bytes) -> bool:
    """
    Return True if the byte-stream uses CRLF endings exclusively.

    The check ensures:
      * At least one CRLF is present.
      * No bare LF (\n not preceded by \r) occurs.
    """
    if b"\r\n" not in data:
        return False
    # Look for a '\n' that is NOT immediately preceded by '\r'
    return re.search(rb"(?<!\r)\n", data) is None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directory_layout_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Project root directory {PROJECT_ROOT} is missing."
    )
    assert SOURCE_DIR.is_dir(), (
        f"Source directory {SOURCE_DIR} is missing."
    )


def test_source_directory_permissions():
    expected_perm = 0o755
    perm = _perm(SOURCE_DIR)
    assert perm == expected_perm, (
        f"{SOURCE_DIR} permissions must be {oct(expected_perm)}, "
        f"found {oct(perm)}."
    )


@pytest.mark.parametrize("filename", sorted(PROPERTIES_FILES))
def test_each_properties_file_exists(filename):
    fpath = SOURCE_DIR / filename
    assert fpath.is_file(), f"Expected file {fpath} is missing."


@pytest.mark.parametrize("filename", sorted(PROPERTIES_FILES))
def test_properties_files_permissions(filename):
    fpath = SOURCE_DIR / filename
    expected_perm = 0o644
    perm = _perm(fpath)
    assert perm == expected_perm, (
        f"{fpath} permissions must be {oct(expected_perm)}, "
        f"found {oct(perm)}."
    )


@pytest.mark.parametrize("filename", sorted(PROPERTIES_FILES))
def test_properties_files_contain_crlf_line_endings(filename):
    fpath = SOURCE_DIR / filename
    data = fpath.read_bytes()
    assert _has_only_crlf(data), (
        f"{fpath} must use Windows style CRLF line endings exclusively "
        f"(\\r\\n)."
    )


def test_readme_exists_and_is_utf8():
    assert README_FILE.is_file(), f"README file {README_FILE} is missing."

    # Decode must succeed with UTF-8 and file must *not* contain CRLF.
    data = README_FILE.read_bytes()

    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(f"{README_FILE} is expected to be UTF-8 encoded.")

    assert b"\r\n" not in data, (
        f"{README_FILE} should use Unix LF line endings, CRLF found."
    )

    expected_perm = 0o644
    perm = _perm(README_FILE)
    assert perm == expected_perm, (
        f"{README_FILE} permissions must be {oct(expected_perm)}, "
        f"found {oct(perm)}."
    )