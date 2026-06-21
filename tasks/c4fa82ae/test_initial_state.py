# test_initial_state.py
"""
pytest suite that validates the initial OS / filesystem state **before** the
student performs any action for the “French-language update” task.

The tests assert that:
1. The required source files and parent directory hierarchy exist.
2. The contents of each prerequisite file are **exactly** as described
   (including the presence of a single LF “\n” at the end of every line).
3. The TSV structure (number of columns, header names, row counts) is correct.

Per the grading specification we intentionally do **not** check for the
presence (or absence) of the expected output file
`/home/user/project/localization/fr_release.tsv`.
"""

import os
import pathlib
import pytest

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

LOCALIZATION_DIR = pathlib.Path("/home/user/project/localization")
MASTER_FILE = LOCALIZATION_DIR / "translations_master.tsv"
UPDATES_FILE = LOCALIZATION_DIR / "fr_updates.tsv"

# ---------------------------------------------------------------------------
# Expected file contents (each string already includes its trailing '\n')
# ---------------------------------------------------------------------------

EXPECTED_MASTER_LINES = [
    "key\ten_US\tfr_FR\tes_ES\n",
    "greeting\tHello\tBonjour\tHola\n",
    "farewell\tGoodbye\tAu revoir\tAdiós\n",
    "thanks\tThank you\tMerci\tGracias\n",
    "yes\tYes\tOui\tSí\n",
    "no\tNo\tNon\tNo\n",
]

EXPECTED_UPDATES_LINES = [
    "fr_FR\n",
    "Salut\n",
    "Au revoir\n",
    "Merci\n",
    "Oui\n",
    "Non\n",
]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file_lines(path: pathlib.Path):
    """Read the file and return a list of lines (including their '\n')."""
    with path.open("r", encoding="utf-8", newline="") as fh:
        return fh.readlines()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_localization_directory_exists():
    assert LOCALIZATION_DIR.is_dir(), (
        f"Expected directory {LOCALIZATION_DIR} to exist."
    )


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (MASTER_FILE, "translations_master.tsv"),
        (UPDATES_FILE, "fr_updates.tsv"),
    ],
)
def test_required_files_exist(path_obj, description):
    assert path_obj.is_file(), (
        f"Required file {path_obj} ({description}) is missing."
    )


def test_master_file_contents_exact():
    lines = read_file_lines(MASTER_FILE)
    assert lines == EXPECTED_MASTER_LINES, (
        f"File {MASTER_FILE} does not match the expected content.\n"
        f"Expected ({len(EXPECTED_MASTER_LINES)} lines):\n{EXPECTED_MASTER_LINES}\n"
        f"Found ({len(lines)} lines):\n{lines}"
    )


def test_updates_file_contents_exact():
    lines = read_file_lines(UPDATES_FILE)
    assert lines == EXPECTED_UPDATES_LINES, (
        f"File {UPDATES_FILE} does not match the expected content.\n"
        f"Expected ({len(EXPECTED_UPDATES_LINES)} lines):\n{EXPECTED_UPDATES_LINES}\n"
        f"Found ({len(lines)} lines):\n{lines}"
    )


def test_master_file_column_counts():
    """
    Ensure every line in translations_master.tsv contains exactly four TAB-separated
    columns: key, en_US, fr_FR, es_ES.
    """
    for idx, line in enumerate(read_file_lines(MASTER_FILE), start=1):
        cols = line.rstrip("\n").split("\t")
        assert len(cols) == 4, (
            f"{MASTER_FILE}: line {idx} has {len(cols)} columns; expected 4."
        )


def test_updates_file_column_counts():
    """
    Ensure every line in fr_updates.tsv contains exactly one column (no TABs).
    """
    for idx, line in enumerate(read_file_lines(UPDATES_FILE), start=1):
        cols = line.rstrip("\n").split("\t")
        assert len(cols) == 1, (
            f"{UPDATES_FILE}: line {idx} has {len(cols)} columns; expected 1."
        )


def test_header_consistency():
    """
    Confirm that the headers of both source files are as documented.
    """
    master_header = read_file_lines(MASTER_FILE)[0]
    updates_header = read_file_lines(UPDATES_FILE)[0]

    assert master_header == "key\ten_US\tfr_FR\tes_ES\n", (
        f"Unexpected header in {MASTER_FILE!s}: {master_header!r}"
    )
    assert updates_header == "fr_FR\n", (
        f"Unexpected header in {UPDATES_FILE!s}: {updates_header!r}"
    )


def test_row_count_alignment():
    """
    The update file must have the same number of data rows as the master file
    so that paste/cut operations can align them correctly.
    """
    master_data_rows = len(EXPECTED_MASTER_LINES) - 1  # exclude header
    updates_data_rows = len(EXPECTED_UPDATES_LINES) - 1

    assert master_data_rows == updates_data_rows, (
        f"Mismatch in data-row counts: {MASTER_FILE} has {master_data_rows} "
        f"rows, but {UPDATES_FILE} has {updates_data_rows} rows."
    )