# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state that must be
# present *before* the student starts working on the assignment.  It checks
# only for the required input artefacts and their exact contents; it does **not**
# touch or look for any of the output paths that the student is expected to
# create later.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
EMP_FILE = DATA_DIR / "employees.csv"
SAL_FILE = DATA_DIR / "salaries.csv"


@pytest.fixture(scope="module")
def expected_employees_lines():
    """Return the canonical contents of employees.csv, split into lines."""
    return [
        "id,name,department,hire_date",
        "1,Alice Zephyr,Engineering,2019-03-14",
        "2,Bob Yellow,Sales,2018-07-22",
        "3,Charlie Xander,Engineering,2020-11-03",
        "4,Diana White,HR,2017-01-30",
        "5,Edward Violet,Engineering,2016-05-12",
        "6,Frida Umber,Sales,2021-09-08",
    ]


@pytest.fixture(scope="module")
def expected_salaries_lines():
    """Return the canonical contents of salaries.csv, split into lines."""
    return [
        "id,year,amount",
        "1,2021,68000",
        "1,2022,72000",
        "2,2022,69000",
        "3,2022,88000",
        "4,2022,65000",
        "5,2021,70000",
        "5,2022,91000",
        "6,2022,73000",
    ]


def _read_csv_lines(path: Path):
    """Read a CSV file and return a list of lines with trailing newlines stripped."""
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n\r") for line in fh]


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing. "
        "Create it or place the CSV files in the correct location."
    )


def test_employees_csv_exists_and_contents(expected_employees_lines):
    assert EMP_FILE.is_file(), f"Missing required file: {EMP_FILE}"
    actual = _read_csv_lines(EMP_FILE)
    assert actual == expected_employees_lines, (
        f"Contents of {EMP_FILE} do not match the expected canonical dataset.\n"
        "If you modified this file, restore it to its original state."
    )


def test_salaries_csv_exists_and_contents(expected_salaries_lines):
    assert SAL_FILE.is_file(), f"Missing required file: {SAL_FILE}"
    actual = _read_csv_lines(SAL_FILE)
    assert actual == expected_salaries_lines, (
        f"Contents of {SAL_FILE} do not match the expected canonical dataset.\n"
        "If you modified this file, restore it to its original state."
    )


def test_csv_are_readable():
    """Sanity check: we must be able to open both CSV files for reading."""
    for csv_path in (EMP_FILE, SAL_FILE):
        try:
            with csv_path.open("r", encoding="utf-8") as fh:
                fh.readline()
        except Exception as exc:  # pragma: no cover
            pytest.fail(f"Cannot read {csv_path}: {exc}")