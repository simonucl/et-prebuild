# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state **before** the student
begins the workflow described in the assignment.

It confirms that only the pre-existing input data is present and that no
output-related paths have been created yet.
"""

from pathlib import Path
import pytest

HOME = Path("/home/user")
RAW_DIR = HOME / "raw_data"

EXPECTED_CSV_FILES = {
    "images_meta.csv",
    "labels.csv",
    "train_split.csv",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #


def read_first_line(path: Path) -> str:
    """Return the first line (stripped of its trailing newline) of a file."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.readline().rstrip("\n")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_raw_data_directory_exists():
    assert RAW_DIR.exists(), f"Directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"Expected {RAW_DIR} to be a directory."


def test_raw_data_contains_exact_expected_files():
    actual_files = {p.name for p in RAW_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_CSV_FILES - actual_files
    extra = actual_files - EXPECTED_CSV_FILES

    assert not missing, (
        f"The following required CSV file(s) are missing from {RAW_DIR}: "
        f"{', '.join(sorted(missing))}"
    )

    assert not extra, (
        f"The directory {RAW_DIR} contains unexpected file(s): "
        f"{', '.join(sorted(extra))}. Only {', '.join(sorted(EXPECTED_CSV_FILES))} "
        f"should be present."
    )


@pytest.mark.parametrize("csv_name,expected_header", [
    ("images_meta.csv", "id,height,width"),
    ("labels.csv", "id,label"),
    ("train_split.csv", "id,split"),
])
def test_each_csv_has_correct_header(csv_name, expected_header):
    csv_path = RAW_DIR / csv_name
    assert csv_path.exists(), f"Expected file {csv_path} to exist."
    assert csv_path.is_file(), f"{csv_path} should be a regular file."
    assert csv_path.stat().st_size > 0, f"{csv_path} appears to be empty."

    header = read_first_line(csv_path)
    assert header == expected_header, (
        f"{csv_path} has an unexpected header.\n"
        f"Expected: {expected_header!r}\n"
        f"Found:    {header!r}"
    )


def test_no_output_paths_exist_yet():
    """
    Ensure that the student has not (yet) created any of the output paths that
    the later stages of the assignment will generate.
    """
    output_paths = [
        HOME / "archive",
        HOME / "prepared_data",
        HOME / "compression_extraction.log",
    ]
    present = [p for p in output_paths if p.exists()]
    assert not present, (
        "The following output path(s) already exist, but should not be present "
        "before the workflow is executed:\n" +
        "\n".join(str(p) for p in present)
    )