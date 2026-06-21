# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem/OS state **before**
# the learner begins the data-cleaning task.  It purposefully ignores every
# file that will be produced during the exercise (cleaned.csv, processing.log,
# error.log, …) and focuses solely on the required starting artefacts.

import os
from pathlib import Path

DATASETS_DIR = Path("/home/user/datasets")
RAW_CSV_PATH = DATASETS_DIR / "raw.csv"

# --------------------------------------------------------------------------- #
# Helper                                                                    #
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    """Return file contents as text.  Fail early if the file is unreadable."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")
    except PermissionError:
        pytest.fail(f"Required file is not readable due to permission issues: {path}")


# --------------------------------------------------------------------------- #
# Tests                                                                      #
# --------------------------------------------------------------------------- #
def test_datasets_directory_exists():
    assert DATASETS_DIR.is_dir(), (
        f"Directory {DATASETS_DIR} must exist.  "
        "Create it and place raw.csv inside it."
    )


def test_raw_csv_exists():
    assert RAW_CSV_PATH.is_file(), (
        f"Initial CSV file is missing: {RAW_CSV_PATH}\n"
        "It must be present before the cleaning step begins."
    )


def test_raw_csv_content():
    expected_content = (
        "id,name,age,score\n"
        "1,Alice,30,85\n"
        "2,Bob,,90\n"
        "3,Charlie,25,\n"
        "4,,27,88\n"
        "5,David,22,92\n"
    )

    actual_content = read_text(RAW_CSV_PATH)

    # 1. Exact text comparison (guarantees header, data rows, order, separators,
    #    newline endings, *and* presence of a final trailing newline).
    assert (
        actual_content == expected_content
    ), (
        f"Content of {RAW_CSV_PATH} does not match the expected initial dataset.\n"
        "Make sure the file contains exactly the following (including the final "
        "newline):\n\n"
        f"{expected_content}"
    )

    # 2. Defensive check: final char must be a newline.
    assert actual_content.endswith("\n"), (
        f"{RAW_CSV_PATH} must end with a single trailing newline."
    )


def test_no_unexpected_files_in_datasets_dir():
    """
    As a courtesy sanity check, ensure that the datasets directory does not
    already contain *extra* files that could interfere with the learner’s
    solution.  Editor swap/backup files (e.g. *.swp, *~) are ignored.
    """
    allowed = {"raw.csv"}
    for p in DATASETS_DIR.iterdir():
        if p.is_file() and p.name not in allowed and not p.name.endswith(("~", ".swp")):
            pytest.fail(
                f"Unexpected file found in {DATASETS_DIR}: {p.name}\n"
                "The directory should initially contain only raw.csv."
            )