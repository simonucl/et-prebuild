# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating
# system / filesystem **before** the student performs any actions for
# the “East Widget sales extraction” task.
#
# The tests assert that:
#   • The required source directory and CSV files exist and contain the
#     exact, unaltered data that the grader will rely on.
#   • No output artefacts from the student solution are present yet.
#
# Only Python’s standard library and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"
OUTPUT_DIR = HOME / "output"

Q1_PATH = DATASETS_DIR / "sales_q1.csv"
Q2_PATH = DATASETS_DIR / "sales_q2.csv"

EXPECTED_Q1_LINES = [
    b"Date,Region,Product,Units,Unit_Price\n",
    b"2023-01-05,East,Widget A,120,9.50\n",
    b"2023-01-07,West,Widget B,200,9.50\n",
    b"2023-02-11,East,Thingamajig,75,15.00\n",
    b"2023-03-02,East,Widget Pro,60,12.00\n",
    b"2023-03-09,South,Widget A,110,9.50\n",
]

EXPECTED_Q2_LINES = [
    b"Date,Region,Product,Units,Unit_Price\n",
    b"2023-04-15,East,Widget A,90,9.50\n",
    b"2023-05-03,North,Gadget,150,8.00\n",
    b"2023-05-22,East,Widget Plus,50,11.00\n",
    b"2023-06-12,East,Thingamajig,40,15.00\n",
    b"2023-06-25,West,Widget A,130,9.50\n",
]

OUTPUT_CSV = OUTPUT_DIR / "east_widget_sales.csv"
OUTPUT_LOG = OUTPUT_DIR / "extraction.log"


def _read_binary_lines(path: Path):
    """Utility: read file as raw bytes and return list of lines."""
    with path.open("rb") as f:
        return f.readlines()


@pytest.mark.parametrize(
    "path",
    [DATASETS_DIR, Q1_PATH, Q2_PATH],
)
def test_required_paths_exist(path: Path):
    """Datasets directory and both CSV files must already exist."""
    assert path.exists(), f"Required path is missing: {path}"


def test_datasets_dir_is_directory():
    assert DATASETS_DIR.is_dir(), f"{DATASETS_DIR} should be a directory."


@pytest.mark.parametrize(
    "csv_path, expected_lines",
    [
        (Q1_PATH, EXPECTED_Q1_LINES),
        (Q2_PATH, EXPECTED_Q2_LINES),
    ],
)
def test_source_csv_contents(csv_path: Path, expected_lines):
    """
    Verify that each source CSV file exists, is readable,
    and byte-for-byte matches the expected fixture data.
    """
    assert csv_path.is_file(), f"Expected file not found: {csv_path}"
    lines = _read_binary_lines(csv_path)
    assert (
        lines == expected_lines
    ), (
        f"Contents of {csv_path} do not match the expected fixture.\n"
        f"Expected {len(expected_lines)} lines, found {len(lines)}."
    )
    # Explicitly ensure every line, including the last, ends with LF.
    assert all(
        ln.endswith(b"\n") for ln in lines
    ), f"{csv_path} must use Unix newlines (LF) on every line."


@pytest.mark.parametrize(
    "output_path",
    [OUTPUT_CSV, OUTPUT_LOG],
)
def test_output_files_do_not_exist_yet(output_path: Path):
    """
    Before the student runs their solution, the consolidated output files
    must *not* exist.  This guards against stale artefacts influencing
    grading.
    """
    assert not output_path.exists(), (
        f"Output file {output_path} already exists before the task is run.  "
        "Please remove any pre-existing artefacts."
    )