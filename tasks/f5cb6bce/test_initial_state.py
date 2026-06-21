# test_initial_state.py
#
# This pytest suite validates the initial state of the operating system /
# file-system *before* the student performs any actions.
#
# It purposely checks ONLY the pre-existing artefacts that must be present
# at the start of the assignment and deliberately avoids touching or
# asserting anything about the artefacts that the student is expected to
# create later on.

import io
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
DATASETS_DIR = HOME / "datasets"

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_utf8_lines(file_path: pathlib.Path):
    """
    Read a text file strictly as UTF-8 and return the list of lines *without*
    trailing newline characters.

    Raises:
        UnicodeDecodeError if the file is not valid UTF-8.
    """
    with file_path.open("r", encoding="utf-8") as fh:
        # Use io.TextIOWrapper semantics to ensure UTF-8 correctness
        return [line.rstrip("\n") for line in fh.readlines()]


# --------------------------------------------------------------------------- #
# Expected reference data (exact content, including order)
# --------------------------------------------------------------------------- #
EXPECTED_A_LINES = [
    "sample_id,condition,value",
    "S1,control,0.50",
    "S2,treatment,1.20",
    "S3,treatment,1.10",
    "S4,control,0.45",
    "S5,treatment,1.30",
]

EXPECTED_B_LINES = [
    "sample_id,condition,value",
    "B1,control,0.55",
    "B2,control,0.60",
    "B3,treatment,1.25",
    "B4,treatment,1.15",
    "B5,control,0.58",
]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_datasets_directory_exists_and_is_directory():
    assert DATASETS_DIR.exists(), (
        f"Required directory {DATASETS_DIR} is missing. "
        "It should have been pre-populated during task initialisation."
    )
    assert DATASETS_DIR.is_dir(), (
        f"{DATASETS_DIR} exists but is not a directory."
    )


@pytest.mark.parametrize(
    "filename,expected_lines",
    [
        ("experimentsA.csv", EXPECTED_A_LINES),
        ("experimentsB.csv", EXPECTED_B_LINES),
    ],
)
def test_dataset_files_exist_and_have_exact_content(filename, expected_lines):
    file_path = DATASETS_DIR / filename
    assert file_path.exists(), (
        f"Pre-existing dataset file {file_path} is missing."
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file."
    )

    # Ensure file can be read as valid UTF-8 and has the expected content
    try:
        lines = read_utf8_lines(file_path)
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"File {file_path} is not valid UTF-8: {exc}"
        )

    assert lines == expected_lines, (
        f"Content of {file_path} does not match the expected reference data.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        + "\n".join(expected_lines)
        + "\n\nActual ({len(lines)} lines):\n"
        + "\n".join(lines)
    )