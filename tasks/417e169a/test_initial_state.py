# test_initial_state.py
"""
Pytest suite that validates the initial, pre-task state of the filesystem
for the “diagnostics snapshot” exercise.

Checked items
-------------
1. /home/user/diagnostics exists and is a directory.
2. The three diagnostic files exist as regular files:
      * /home/user/diagnostics/cpu_dump.txt
      * /home/user/diagnostics/mem_dump.txt
      * /home/user/diagnostics/disk_dump.txt
3. Each diagnostic file:
      * Contains exactly three non-blank lines.
      * Every line matches the pattern  "<Key>: <Value>"
        ‑ exactly one literal colon followed by a single space.
      * Keys and values themselves contain no additional colon.
      * No line has trailing whitespace.
The tests deliberately avoid touching /home/user/output or any other
post-task artefacts, in accordance with the grading rules.
"""
from pathlib import Path
import re
import pytest

DIAG_DIR = Path("/home/user/diagnostics")
FILES = [
    DIAG_DIR / "cpu_dump.txt",
    DIAG_DIR / "mem_dump.txt",
    DIAG_DIR / "disk_dump.txt",
]

LINE_REGEX = re.compile(r"^[^:\s][^:]*: [^:\s].*$")


def test_diagnostics_directory_exists():
    assert DIAG_DIR.exists(), f"Required directory {DIAG_DIR} is missing."
    assert DIAG_DIR.is_dir(), f"{DIAG_DIR} exists but is not a directory."


@pytest.mark.parametrize("file_path", FILES, ids=[p.name for p in FILES])
def test_diagnostic_file_exists_and_is_file(file_path: Path):
    assert file_path.exists(), f"Required file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."


@pytest.mark.parametrize("file_path", FILES, ids=[p.name for p in FILES])
def test_file_has_exactly_three_well_formed_lines(file_path: Path):
    contents = file_path.read_text(encoding="utf-8").splitlines()
    assert len(contents) == 3, (
        f"{file_path} should contain exactly 3 lines, found {len(contents)}."
    )

    for idx, line in enumerate(contents, start=1):
        # General pattern check
        assert LINE_REGEX.match(line), (
            f"Line {idx} in {file_path} does not match "
            f"the required 'Key: Value' format: {line!r}"
        )

        # Ensure no trailing spaces or tabs
        assert line == line.rstrip(" \t"), (
            f"Line {idx} in {file_path} has trailing whitespace: {line!r}"
        )

        # Ensure the line contains exactly one colon
        assert line.count(":") == 1, (
            f"Line {idx} in {file_path} must contain exactly one colon: {line!r}"
        )