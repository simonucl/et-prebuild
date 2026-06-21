# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system /
# file-system BEFORE the student performs any actions for the “fast_linecount”
# exercise.
#
# Restrictions (as required by the auto-grader):
#   * Uses only the Python standard library + pytest
#   * Does NOT look for, touch or even mention any of the files / directories
#     that the student is supposed to create later (e.g. /home/user/tools/*)
#   * Provides clear, actionable failure messages when expectations are not met
#
# What **is** verified here:
#   1. Presence and contents of the slow reference script
#   2. Presence and expected line counts of the two sample data files
#
# Author: auto-generated for the grading harness

import os
from pathlib import Path

SLOW_SCRIPT = Path("/home/user/scripts/slow_linecount.sh")
DATA_FILE_1 = Path("/home/user/data/file1.txt")
DATA_FILE_2 = Path("/home/user/data/file2.txt")

EXPECTED_LINECOUNT_FILE1 = 10_000
EXPECTED_LINECOUNT_FILE2 = 15_000


def _read_file_lines(path: Path):
    "Helper: returns list of lines from *path* decoded with UTF-8."
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


def test_slow_script_exists_and_is_regular_file():
    assert SLOW_SCRIPT.exists(), (
        f"Expected reference script '{SLOW_SCRIPT}' to exist, "
        "but it is missing."
    )
    assert SLOW_SCRIPT.is_file(), (
        f"Expected '{SLOW_SCRIPT}' to be a regular file."
    )


def test_slow_script_has_correct_shebang_and_uses_cat():
    content = _read_file_lines(SLOW_SCRIPT)
    assert content, f"File '{SLOW_SCRIPT}' is unexpectedly empty."

    first_line = content[0].rstrip("\n")
    assert first_line == "#!/bin/bash", (
        f"First line of '{SLOW_SCRIPT}' must be '#!/bin/bash' "
        f"but found: {first_line!r}"
    )

    full_text = "".join(content)
    assert "cat" in full_text, (
        f"Reference script '{SLOW_SCRIPT}' should use the slow approach "
        "by invoking the external command 'cat', but no such usage was found."
    )
    assert "wc -l" in full_text, (
        "Reference script should ultimately pipe to 'wc -l', "
        "but that pattern was not found."
    )


def test_data_files_exist():
    for path in (DATA_FILE_1, DATA_FILE_2):
        assert path.exists(), f"Expected data file '{path}' to exist."
        assert path.is_file(), f"'{path}' is not a regular file."


def test_data_file1_has_expected_number_of_lines():
    line_count = sum(1 for _ in DATA_FILE_1.open("r", encoding="utf-8"))
    assert (
        line_count == EXPECTED_LINECOUNT_FILE1
    ), f"{DATA_FILE_1} should have {EXPECTED_LINECOUNT_FILE1:,} lines, found {line_count:,}."


def test_data_file2_has_expected_number_of_lines():
    line_count = sum(1 for _ in DATA_FILE_2.open("r", encoding="utf-8"))
    assert (
        line_count == EXPECTED_LINECOUNT_FILE2
    ), f"{DATA_FILE_2} should have {EXPECTED_LINECOUNT_FILE2:,} lines, found {line_count:,}."