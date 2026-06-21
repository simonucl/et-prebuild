# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the filesystem
# before the student performs any action.  It checks that the CI
# workspace is laid out exactly as described and that only the three
# specific “*.tmp” files contain the string “UNSAFE”.
#
# NOTE:  The suite intentionally makes **no reference** to the expected
#        output file (/home/user/ci_temp/unsafe_tmp_files.txt) so that it
#        does not interfere with the student’s forthcoming work.

import os
from pathlib import Path

import pytest

CI_ROOT = Path("/home/user/ci_temp").expanduser().resolve()

# ----------------------------------------------------------------------
# Helper data
# ----------------------------------------------------------------------

EXPECTED_DIRS = [
    CI_ROOT,
    CI_ROOT / "build1",
    CI_ROOT / "build2",
    CI_ROOT / "build3",
    CI_ROOT / "build3" / "nested",
]

EXPECTED_FILES = [
    CI_ROOT / "build1" / "artifact1.tmp",
    CI_ROOT / "build1" / "keep.txt",
    CI_ROOT / "build1" / "notes.tmp",
    CI_ROOT / "build2" / "debug.tmp",
    CI_ROOT / "build2" / "noise.tmp",
    CI_ROOT / "build2" / "other.log",
    CI_ROOT / "build3" / "nested" / "inner.log",
    CI_ROOT / "build3" / "nested" / "inner.tmp",
]

UNSAFE_TMP_FILES = {
    CI_ROOT / "build1" / "artifact1.tmp",
    CI_ROOT / "build2" / "debug.tmp",
    CI_ROOT / "build3" / "nested" / "inner.tmp",
}

SAFE_TMP_FILES = {
    CI_ROOT / "build1" / "notes.tmp",
    CI_ROOT / "build2" / "noise.tmp",
}

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

@pytest.mark.parametrize("directory", EXPECTED_DIRS)
def test_expected_directories_exist(directory):
    assert directory.is_dir(), f"Required directory missing: {directory}"


@pytest.mark.parametrize("filepath", EXPECTED_FILES)
def test_expected_files_exist(filepath):
    assert filepath.is_file(), f"Required file missing: {filepath}"


@pytest.mark.parametrize("filepath", list(UNSAFE_TMP_FILES))
def test_files_with_unsafe_marker_contain_it(filepath):
    """
    The specified .tmp files must contain the literal substring 'UNSAFE'.
    """
    content = filepath.read_text(encoding="utf-8", errors="ignore")
    assert "UNSAFE" in content, (
        f"File {filepath} is expected to contain the string 'UNSAFE', "
        "but it does not."
    )


@pytest.mark.parametrize("filepath", list(SAFE_TMP_FILES))
def test_other_tmp_files_do_not_contain_unsafe(filepath):
    """
    The other .tmp files must *not* contain the substring 'UNSAFE'.
    """
    content = filepath.read_text(encoding="utf-8", errors="ignore")
    assert "UNSAFE" not in content, (
        f"File {filepath} unexpectedly contains the string 'UNSAFE'."
    )


def test_exact_set_of_unsafe_tmp_files():
    """
    Ensure that *exactly* the three expected .tmp files contain 'UNSAFE'
    and that no additional .tmp files under the workspace include it.
    """
    found_unsafe = {
        path
        for path in CI_ROOT.rglob("*.tmp")
        if "UNSAFE" in path.read_text(encoding="utf-8", errors="ignore")
    }

    assert (
        found_unsafe == UNSAFE_TMP_FILES
    ), (
        "The set of '*.tmp' files that contain 'UNSAFE' does not match the "
        "expected list.\n"
        f"Expected:\n  {sorted(map(str, UNSAFE_TMP_FILES))}\n"
        f"Found:\n  {sorted(map(str, found_unsafe))}"
    )