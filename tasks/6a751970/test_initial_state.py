# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must
# exist **before** the student starts working.  It makes sure the two
# raw TSV exports are present and correct, and that no output directory
# has been created yet.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"
CLEANED_DIR = HOME / "cleaned"

FILE_2022 = DATASETS_DIR / "survey_2022.tsv"
FILE_2023 = DATASETS_DIR / "survey_2023.tsv"


@pytest.fixture(scope="module")
def expected_files_content():
    """Return the exact expected content (without trailing newline)
    for the two source TSV files."""
    expected_2022 = """id\tname\tage\tgender\tcountry\tincome\thired_date
101\tAnna\t28\tF\tUSA\t65000\t2021-05-10
102\tBen\t34\tM\tCanada\t72000\t2019-09-13
103\tChloé\t25\tF\tFrance\t58000\t2020-06-22
104\tDavid\t40\tM\tUSA\t80000\t2018-02-14
105\tElla\t31\tF\tUK\t69000\t2022-01-03"""
    expected_2023 = """id\tname\tdepartment\tsatisfaction_score\tpromotion_eligible
101\tAnna\tSales\t4\tYes
102\tBen\tMarketing\t5\tNo
103\tChloé\tSupport\t3\tYes
104\tDavid\tEngineering\t4\tNo
105\tElla\tHR\t5\tYes"""
    return {
        FILE_2022: expected_2022,
        FILE_2023: expected_2023,
    }


def _read_file_strip(path: Path) -> str:
    """Read a file and strip exactly one trailing newline if present."""
    with path.open("r", encoding="utf-8") as fh:
        data = fh.read()
    # Remove a single trailing newline so we can compare robustly
    return data[:-1] if data.endswith("\n") else data


def test_source_files_exist_and_are_regular():
    assert FILE_2022.exists(), f"{FILE_2022} is missing"
    assert FILE_2023.exists(), f"{FILE_2023} is missing"
    assert FILE_2022.is_file(), f"{FILE_2022} is not a regular file"
    assert FILE_2023.is_file(), f"{FILE_2023} is not a regular file"


def test_cleaned_dir_not_present_yet():
    assert not CLEANED_DIR.exists(), (
        f"{CLEANED_DIR} should NOT exist before the student runs the task"
    )


@pytest.mark.parametrize("path", [FILE_2022, FILE_2023])
def test_file_content_exact(path: Path, expected_files_content):
    expected = expected_files_content[path]
    actual = _read_file_strip(path)
    assert (
        actual == expected
    ), f"Content of {path} does not match the expected initial dataset."


@pytest.mark.parametrize(
    "path, expected_cols, expected_rows",
    [
        (FILE_2022, 7, 5),  # header + 5 data rows, 7 columns
        (FILE_2023, 5, 5),  # header + 5 data rows, 5 columns
    ],
)
def test_tsv_structure(path: Path, expected_cols: int, expected_rows: int):
    raw = _read_file_strip(path)
    lines = raw.split("\n")
    header, data_rows = lines[0], lines[1:]

    # Column count
    header_cols = header.split("\t")
    assert len(header_cols) == expected_cols, (
        f"{path} should have {expected_cols} columns, "
        f"found {len(header_cols)} instead"
    )

    # Data‐row count
    assert len(data_rows) == expected_rows, (
        f"{path} should have {expected_rows} data rows, "
        f"found {len(data_rows)} instead"
    )

    # Ensure every data row has the expected number of columns
    for idx, row in enumerate(data_rows, start=1):
        cols = row.split("\t")
        assert len(cols) == expected_cols, (
            f"{path}: row #{idx} has {len(cols)} columns; "
            f"expected {expected_cols}"
        )

    # Ensure ids are unique
    ids = [row.split("\t")[0] for row in data_rows]
    assert len(ids) == len(set(ids)), f"{path} contains duplicate id values"