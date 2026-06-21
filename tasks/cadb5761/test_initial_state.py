# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student begins working on the assignment.
#
# It checks ONLY the items that are guaranteed to exist up-front:
#   • the raw_sales directory
#   • the three CSV input files and their **exact** contents
#
# It deliberately does NOT check for any output files, output directories,
# scripts, cron jobs, or log files, because those will be created by the
# student as part of the task.

import pathlib
import textwrap

import pytest

RAW_SALES_DIR = pathlib.Path("/home/user/data/raw_sales")

# Expected files and their contents (final newlines are ignored for comparison)
EXPECTED_CSV_FILES = {
    RAW_SALES_DIR / "sales_2023-03-01.csv": textwrap.dedent(
        """\
        date,product,units,unit_price
        2023-03-01,Widget,10,25.50
        2023-03-01,Gadget,5,40.00
        """
    ),
    RAW_SALES_DIR / "sales_2023-03-02.csv": textwrap.dedent(
        """\
        date,product,units,unit_price
        2023-03-02,Widget,8,25.50
        2023-03-02,Thingamajig,3,60.00
        """
    ),
    RAW_SALES_DIR / "sales_2023-03-03.csv": textwrap.dedent(
        """\
        date,product,units,unit_price
        2023-03-03,Gadget,7,40.00
        2023-03-03,Thingamajig,2,60.00
        """
    ),
}


def normalize(text: str) -> str:
    """
    Normalise line endings and strip trailing blank lines
    so the comparison is OS-agnostic and tolerant of a
    single trailing newline.
    """
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines())


def test_raw_sales_directory_exists():
    """The /home/user/data/raw_sales/ directory must already exist."""
    assert RAW_SALES_DIR.exists(), (
        f"Expected directory {RAW_SALES_DIR} to exist, "
        "but it is missing."
    )
    assert RAW_SALES_DIR.is_dir(), (
        f"{RAW_SALES_DIR} exists but is not a directory."
    )


@pytest.mark.parametrize("file_path", list(EXPECTED_CSV_FILES.keys()))
def test_csv_file_exists(file_path: pathlib.Path):
    """Each expected CSV file must already be present."""
    assert file_path.exists(), (
        f"Expected file {file_path} to exist, but it is missing."
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file."
    )


@pytest.mark.parametrize(
    ("file_path", "expected_content"), EXPECTED_CSV_FILES.items()
)
def test_csv_file_contents(file_path: pathlib.Path, expected_content: str):
    """
    The contents of each CSV file must match exactly what the task
    description specifies.
    """
    actual_content = file_path.read_text(encoding="utf-8")
    assert (
        normalize(actual_content) == normalize(expected_content)
    ), (
        f"Contents of {file_path} do not match the expected input data.\n\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )