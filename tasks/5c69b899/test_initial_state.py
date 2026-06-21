# test_initial_state.py
#
# This pytest suite validates that the operating system starts in the
# expected, pristine state **before** the student performs any action.
#
# What we verify:
#   • The source directory /home/user/data exists.
#   • The two required CSV source files exist at the exact paths given.
#   • Each of those files is byte-for-byte identical to the specification.
#
# We intentionally do NOT check for /home/user/output or any files inside it,
# as the student is responsible for creating those during the task.

from pathlib import Path

import pytest

DATA_DIR = Path("/home/user/data")
JAN_FILE = DATA_DIR / "sales_january.csv"
FEB_FILE = DATA_DIR / "sales_february.csv"

EXPECTED_JAN = (
    "Date,Region,Product,Units,Unit_Price\n"
    "2021-01-03,East,Gadget,10,19.99\n"
    "2021-01-05,West,Widget,5,25.00\n"
    "2021-01-10,East,Widget,7,25.00\n"
)

EXPECTED_FEB = (
    "Date,Region,Product,Units,Unit_Price\n"
    "2021-02-12,North,Gadget,3,19.99\n"
    "2021-02-15,East,Widget,9,25.00\n"
    "2021-02-20,East,Gadget,4,19.99\n"
)


def _read_file(path: Path) -> str:
    """
    Helper that returns the full text of a file.

    A separate helper makes it easier to give a precise error message when the
    file is unreadable or has the wrong encoding.
    """
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Expected file {path} to exist, but it is missing.")
    except UnicodeDecodeError:  # pragma: no cover
        pytest.fail(f"File {path} could not be decoded as UTF-8.")


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} does not exist. "
        "It must be present before you start the task."
    )


@pytest.mark.parametrize(
    "path, expected_contents",
    [
        (JAN_FILE, EXPECTED_JAN),
        (FEB_FILE, EXPECTED_FEB),
    ],
)
def test_source_csv_files_exist_and_match_spec(path: Path, expected_contents: str):
    assert path.is_file(), (
        f"Required source file {path} is missing.\n"
        "Make sure the file is located exactly at this path."
    )

    actual_contents = _read_file(path)
    assert (
        actual_contents == expected_contents
    ), (
        f"Contents of {path} do not match the specification.\n\n"
        "Expected:\n"
        f"{expected_contents!r}\n\n"
        "Actual:\n"
        f"{actual_contents!r}"
    )