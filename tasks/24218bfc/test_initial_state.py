# test_initial_state.py
#
# Pytest suite to validate the **initial** filesystem state
# BEFORE the learner starts working on the exercise.
#
# Rules enforced:
#   • Verify that all required input files are present and correct.
#   • Do NOT look for any output files, directories, or scripts that the
#     learner is supposed to create later.
#   • Use only stdlib + pytest.

import pathlib
import pytest

DATA_DIR = pathlib.Path("/home/user/data")

Q1_FILE = DATA_DIR / "raw_sales_2023_Q1.csv"
Q2_FILE = DATA_DIR / "raw_sales_2023_Q2.csv"

EXPECTED_Q1_CONTENT = (
    "product,quantity,price\n"
    "Laptop,10,1200\n"
    "Phone,25,800\n"
    "Tablet,14,600\n"
)

EXPECTED_Q2_CONTENT = (
    "product,quantity,price\n"
    "Laptop,8,1150\n"
    "Phone,30,780\n"
    "Headphones,40,150\n"
)


@pytest.fixture(params=[Q1_FILE, Q2_FILE])
def data_file(request):
    """
    Parametrised fixture that yields each expected data file path.
    """
    return request.param


def test_data_directory_exists():
    """Ensure the /home/user/data directory is present."""
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} does not exist.\n"
        "Create it and place the raw CSV files there."
    )


def test_data_files_exist_and_are_regular(data_file):
    """Check that each expected CSV file exists and is a regular file."""
    assert data_file.exists(), f"Required file {data_file} is missing."
    assert data_file.is_file(), f"{data_file} exists but is not a regular file."


@pytest.mark.parametrize(
    "csv_path, expected_content",
    [
        (Q1_FILE, EXPECTED_Q1_CONTENT),
        (Q2_FILE, EXPECTED_Q2_CONTENT),
    ],
)
def test_csv_contents_exact_match(csv_path, expected_content):
    """
    Verify that the contents of each raw CSV file match the expected
    byte-for-byte string (including trailing newline).
    """
    try:
        content = csv_path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {csv_path}: {exc}")

    assert (
        content == expected_content
    ), (
        f"Contents of {csv_path} do not match the expected fixture.\n\n"
        f"--- Expected ---\n{expected_content!r}\n"
        f"--- Found ---\n{content!r}\n"
        "Make sure you have not modified the original data files."
    )