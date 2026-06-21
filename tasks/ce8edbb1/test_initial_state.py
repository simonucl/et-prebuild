# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state before the
# student carries out any work.  It checks only the presence and exact
# contents of the three source files; it intentionally avoids touching
# /home/user/results or any other output artefacts.

from pathlib import Path
import textwrap
import pytest

HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"

# ---------------------------------------------------------------------------
# Expected, byte-for-byte contents of the three input files.
# The trailing newline shown here **must** also be present on disk.
# ---------------------------------------------------------------------------

EXPECTED_EXPERIMENT_A = textwrap.dedent("""\
    SampleID,Condition,GeneCount,Quality
    S1,control,1523,0.98
    S2,treated,1480,0.95
    S3,control,1601,0.97
    S4,treated,1499,0.96
    S5,control,1588,0.99
    """).lstrip()

EXPECTED_EXPERIMENT_B = textwrap.dedent("""\
    ID,Expression,Dose
    S1,0.83,5
    S2,0.72,10
    S3,0.79,5
    S4,0.75,10
    S5,0.81,5
    """).lstrip()

EXPECTED_NOTES = textwrap.dedent("""\
    Run\tDate\tOperator\tRemark
    1\t2023-03-13\tDr.X\tOK
    2\t2023-03-14\tDr.X\tOK
    3\t2023-03-15\tDr.X\tRetry
    4\t2023-03-16\tDr.X\tOK
    5\t2023-03-17\tDr.X\tOK
    """).lstrip()

FILE_EXPECTATIONS = {
    DATASETS_DIR / "experiment_A.csv": EXPECTED_EXPERIMENT_A,
    DATASETS_DIR / "experiment_B.csv": EXPECTED_EXPERIMENT_B,
    DATASETS_DIR / "notes.tsv": EXPECTED_NOTES,
}

# ---------------------------------------------------------------------------
# Helper(s)
# ---------------------------------------------------------------------------


def read_file(path: Path) -> str:
    """Read a text file using UTF-8 and return its contents."""
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_datasets_directory_exists():
    """The /home/user/datasets directory must already exist."""
    assert DATASETS_DIR.exists(), (
        f"Required directory {DATASETS_DIR} is missing. "
        "All source files should live here."
    )
    assert DATASETS_DIR.is_dir(), f"{DATASETS_DIR} exists but is not a directory."


@pytest.mark.parametrize("file_path, expected_text", FILE_EXPECTATIONS.items())
def test_source_file_exists_with_correct_content(file_path: Path, expected_text: str):
    """Each source file must exist and match the exact expected content."""
    assert file_path.exists(), f"Source file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    actual_text = read_file(file_path)
    # Show a helpful diff if the contents are off.
    assert actual_text == expected_text, (
        f"File {file_path} does not match the expected content.\n"
        "Differences (expected ⟶ actual):\n"
        "--------------------------------"
    )