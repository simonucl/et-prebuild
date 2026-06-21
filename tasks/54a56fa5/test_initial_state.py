# test_initial_state.py
#
# Pytest suite that verifies the expected *initial* filesystem state
# before the learner completes the exercise.  These tests **must pass**
# on the clean starter environment that the autograder provides.

import os
from pathlib import Path

# ---------- Constants ----------
HOME = Path("/home/user")
RAW_DIR = HOME / "datasets" / "raw"
CSV_FILES = {
    "iris.csv": "sepal_length,sepal_width,petal_length,petal_width,species",
    "mtcars.csv": "model,mpg,cyl,disp,hp,drat,wt,qsec,vs,am,gear,carb",
}


# ---------- Helper ----------
def read_first_line(path: Path) -> str:
    """
    Return the first (non-blank) line of a text file, stripped of
    leading/trailing whitespace.  Raises FileNotFoundError if `path`
    does not exist.
    """
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped:  # skip blank lines
                return stripped
    return ""


# ---------- Tests ----------
def test_raw_directory_exists_and_is_directory():
    """Assert that /home/user/datasets/raw exists and is a directory."""
    assert RAW_DIR.exists(), f"Expected directory {RAW_DIR} to exist."
    assert RAW_DIR.is_dir(), f"Expected {RAW_DIR} to be a directory."


def test_required_csv_files_exist_and_are_regular_files():
    """
    Each required CSV file must exist as a regular file directly under
    /home/user/datasets/raw.
    """
    missing = []
    non_regular = []
    for filename in CSV_FILES:
        full_path = RAW_DIR / filename
        if not full_path.exists():
            missing.append(str(full_path))
        elif not full_path.is_file():
            non_regular.append(str(full_path))

    assert not missing, (
        "The following required CSV file(s) are missing:\n  " + "\n  ".join(missing)
    )
    assert not non_regular, (
        "The following path(s) exist but are not regular files:\n  "
        + "\n  ".join(non_regular)
    )


def test_csv_headers_match_expected():
    """
    Quick sanity-check that the first non-blank line of each CSV file matches the
    expected header.  This guards against accidental file corruption.
    """
    mismatches = []
    for filename, expected_header in CSV_FILES.items():
        full_path = RAW_DIR / filename
        try:
            actual_header = read_first_line(full_path)
        except FileNotFoundError:
            # Existence is covered in a separate test; skip here.
            continue

        if actual_header != expected_header:
            mismatches.append(
                f"{full_path}: expected header '{expected_header}', found '{actual_header}'"
            )

    assert not mismatches, (
        "Header mismatch detected in the following CSV file(s):\n  "
        + "\n  ".join(mismatches)
    )