# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state that must be
# present *before* the student starts working on the ETL task.  It deliberately
# avoids checking for any of the expected output artefacts because those do not
# exist yet and will be created by the student.
#
# The tests are intentionally explicit so that any failure message pin-points
# exactly what is missing or incorrect.

from pathlib import Path
import pytest

# --------------------------------------------------------------------------- #
# CONSTANTS                                                                   #
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
ETL_ROOT = HOME / "etl"
INPUT_DIR = ETL_ROOT / "input"
INPUT_FILE = INPUT_DIR / "sales_data.csv"

# Expected byte-for-byte contents of the raw input CSV (including the trailing
# newline after the last record).
EXPECTED_INPUT_CSV = (
    "order_id,customer_id,date,product,quantity,unit_price\n"
    "1001,501,2020-11-10,Laptop,2,799.99\n"
    "1002,502,2021-01-05,Mouse,5,25.50\n"
    "1003,503,2021-03-16,Keyboard,3,45.00\n"
    "1004,504,2020-07-23,Monitor,1,189.99\n"
    "1005,505,2021-12-30,Laptop,1,749.99\n"
)

# --------------------------------------------------------------------------- #
# HELPERS                                                                     #
# --------------------------------------------------------------------------- #


def _read_text(path: Path) -> str:
    """
    Wrapper around Path.read_text() that always reads the file as UTF-8.

    A separate helper keeps the test functions short and the failure messages
    clearer in case the read itself raises.
    """
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


# --------------------------------------------------------------------------- #
# TESTS                                                                       #
# --------------------------------------------------------------------------- #

def test_etl_root_exists():
    assert ETL_ROOT.is_dir(), (
        f"Directory {ETL_ROOT} is missing. It should have been provisioned by "
        "the exercise setup."
    )


def test_input_dir_exists():
    assert INPUT_DIR.is_dir(), (
        f"Directory {INPUT_DIR} is missing. The raw input CSV must reside in "
        "this location."
    )


def test_input_file_exists():
    assert INPUT_FILE.is_file(), (
        f"Expected raw data file {INPUT_FILE} does not exist."
    )


def test_input_file_content_unchanged():
    actual = _read_text(INPUT_FILE)
    assert actual == EXPECTED_INPUT_CSV, (
        f"The contents of {INPUT_FILE} do not match the expected initial CSV "
        "supplied by the exercise. Do **not** modify this file before running "
        "your transformation commands.\n\n"
        "---- Expected ----\n"
        f"{EXPECTED_INPUT_CSV}"
        "----   Got   ----\n"
        f"{actual}"
        "------------------"
    )