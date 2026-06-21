# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present before the student performs any actions for the “customer_churn”
# exercise.  It purposefully checks only the *input* (raw) side of the
# workspace and stays completely silent about the output locations that will
# be created later (backups/, archives/, cleaned_data/, logs/), in accordance
# with the grading-suite rules.

import pathlib
import pytest
import textwrap

HOME = pathlib.Path("/home/user")
CC_BASE = HOME / "projects" / "customer_churn"
RAW_DIR = CC_BASE / "raw_data"

# ---------------------------------------------------------------------------
# Helper: the canonical initial‐state contents of the two CSV files.
# ---------------------------------------------------------------------------

EXPECTED_2021 = textwrap.dedent("""\
    id,name,age,subscription
    1,Alice,30,Basic
    2,Bob,25,Premium
    3,Charlie,35,Basic
    2,Bob,25,Premium

    """)  # note the trailing blank line (empty string after final \n)

EXPECTED_2022 = textwrap.dedent("""\
    id,name,age,subscription
    4,David,40,Premium
    5,Eva,28,Basic
    4,David,40,Premium
    """)  # last line ends with \n but there is no completely blank line


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_raw_data_directory_exists():
    """The only pre-existing directory must be …/raw_data/."""
    assert RAW_DIR.is_dir(), (
        f"Expected directory {RAW_DIR} to exist before starting the task."
    )


@pytest.mark.parametrize(
    "filename,expected_text",
    [
        ("customers_2021.csv", EXPECTED_2021),
        ("customers_2022.csv", EXPECTED_2022),
    ],
)
def test_raw_csv_files_exist_and_match_expected_content(filename, expected_text):
    """
    Each raw CSV file must exist and its byte-content must match the canonical
    initial data provided in the task description.
    """
    csv_path = RAW_DIR / filename
    assert csv_path.is_file(), f"Missing required input file: {csv_path}"

    actual_bytes = csv_path.read_bytes()
    expected_bytes = expected_text.encode("utf-8")
    assert (
        actual_bytes == expected_bytes
    ), f"File {csv_path} does not match the expected initial content."


def test_no_extra_files_in_raw_data():
    """
    Only the two declared CSVs should be present inside …/raw_data/.
    Blank or hidden files would indicate tampering with the initial state.
    """
    expected_files = {"customers_2021.csv", "customers_2022.csv"}
    actual_files = {p.name for p in RAW_DIR.iterdir() if p.is_file()}
    assert actual_files == expected_files, (
        f"Unexpected files in {RAW_DIR}: {sorted(actual_files - expected_files)}"
    )