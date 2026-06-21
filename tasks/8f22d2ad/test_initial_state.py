# test_initial_state.py
#
# Pytest suite that validates the initial workspace state *before* the student
# begins any work.  It checks only the artefacts that must already exist, and
# deliberately avoids asserting anything about files or directories the student
# is expected to create later.

from pathlib import Path
import pytest

# Base paths used throughout the tests
HOME = Path("/home/user")
DEV_ROOT = HOME / "dev_project"
RAW_DATA_DIR = DEV_ROOT / "raw_data"

ALPHA_CSV = RAW_DATA_DIR / "alpha.csv"
BETA_CSV = RAW_DATA_DIR / "beta.csv"


@pytest.mark.parametrize(
    "csv_path,expected_lines",
    [
        (
            ALPHA_CSV,
            [
                "id,name,score",
                "1,Alice,88",
                "2,Bob,92",
                "3,Charlie,67",
            ],
        ),
        (
            BETA_CSV,
            [
                "id,name,score",
                "4,Denise,75",
                "5,Evan,83",
                "6,Faith,91",
            ],
        ),
    ],
)
def test_initial_csv_files_exist_and_are_correct(csv_path: Path, expected_lines):
    """
    Ensure that alpha.csv and beta.csv are present in the raw_data directory
    with the exact expected contents (ignoring trailing newline nuances).
    """
    # 1. Directory existence
    assert RAW_DATA_DIR.is_dir(), (
        f"Expected directory '{RAW_DATA_DIR}' does not exist. "
        "The initial raw data directory must be present."
    )

    # 2. File existence
    assert csv_path.is_file(), (
        f"Expected CSV file '{csv_path}' is missing. "
        "Both alpha.csv and beta.csv must exist before any processing begins."
    )

    # 3. File content
    file_text = csv_path.read_text(encoding="utf-8")
    # Split lines without keeping newline characters to avoid
    # false negatives due to the presence or absence of a final \n.
    actual_lines = file_text.splitlines()

    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of '{csv_path}' do not match the expected initial data.\n"
        f"Expected lines:\n{expected_lines}\n\nActual lines:\n{actual_lines}"
    )


def test_raw_data_directory_contains_only_expected_files():
    """
    The raw_data directory should contain exactly the two expected CSV files
    and nothing else at the outset.
    """
    expected_files = {ALPHA_CSV.name, BETA_CSV.name}
    actual_files = {p.name for p in RAW_DATA_DIR.iterdir() if p.is_file()}

    missing = expected_files - actual_files
    unexpected = actual_files - expected_files

    assert not missing, (
        f"The raw_data directory is missing the following required files: {', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        f"The raw_data directory contains unexpected files that should not be there yet: "
        f"{', '.join(sorted(unexpected))}"
    )