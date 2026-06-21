# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem and metadata
# expected by the assignment are present *before* any student action.
#
# It intentionally does NOT look for (or complain about) any of the artefacts
# that the student is expected to create later (summary/, logs/, etc.).
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

import pytest

# Absolute paths used throughout the tests
META_DIR = Path("/home/user/repos/meta")

# -----------------------------------------------------------------------------


def _read_nonblank_lines(filepath: Path):
    """
    Read a text file as UTF-8 and return a list of its non-blank lines
    (stripped of the trailing newline but otherwise unmodified).
    """
    with filepath.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def test_meta_directory_exists():
    assert META_DIR.is_dir(), f"Required directory {META_DIR} is missing."


def test_expected_meta_files_present_and_no_extras():
    """
    The /home/user/repos/meta directory must contain exactly three .meta files
    with the specified names—and nothing else ending in '.meta'.
    """
    expected_files = {
        META_DIR / "core-tools.meta",
        META_DIR / "core-libs.meta",
        META_DIR / "experimental.meta",
    }

    # Collect actual *.meta files
    actual_files = {p for p in META_DIR.iterdir() if p.suffix == ".meta"}

    missing = expected_files - actual_files
    extras = actual_files - expected_files

    assert not missing, (
        "The following required .meta files are missing:\n  "
        + "\n  ".join(str(p) for p in sorted(missing))
    )
    assert not extras, (
        "Unexpected .meta files found in the meta directory:\n  "
        + "\n  ".join(str(p) for p in sorted(extras))
    )


@pytest.mark.parametrize(
    "file_name, expected_lines",
    [
        (
            "core-tools.meta",
            [
                "a100 core-tools 1.0.0 2048 1111111111111111111111111111111111111111111111111111111111111111",
                "a101 core-tools 1.1.0 1000 2222222222222222222222222222222222222222222222222222222222222222",
                "a102 core-tools 2.0.0 4096 3333333333333333333333333333333333333333333333333333333333333333",
            ],
        ),
        (
            "core-libs.meta",
            [
                "b200 core-libs 1.0.0 5120 4444444444444444444444444444444444444444444444444444444444444444",
                "b201 core-libs 1.2.0 500 5555555555555555555555555555555555555555555555555555555555555555",
            ],
        ),
        (
            "experimental.meta",
            [
                "x300 experimental 0.1.0 2048 6666666666666666666666666666666666666666666666666666666666666666",
            ],
        ),
    ],
)
def test_meta_file_contents(file_name, expected_lines):
    """
    For each .meta file, verify that:
      1. The file exists and is UTF-8 decodable.
      2. All expected lines (non-blank) are present and in the correct order.
      3. No extra non-blank lines are present.
      4. Each non-blank line contains exactly five whitespace-separated fields.
    """
    file_path = META_DIR / file_name
    assert file_path.is_file(), f"Expected file {file_path} is missing."

    lines = _read_nonblank_lines(file_path)

    # 2 & 3 — exact match required
    assert (
        lines == expected_lines
    ), f"Contents of {file_path} do not match the expected lines."

    # 4 — structural validation
    for lineno, line in enumerate(lines, start=1):
        fields = line.split()
        assert len(fields) == 5, (
            f"In {file_path} line {lineno!r} should have exactly 5 fields "
            f"but has {len(fields)}: {line!r}"
        )