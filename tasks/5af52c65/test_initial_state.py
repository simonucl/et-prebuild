# test_initial_state.py
# Pytest suite to verify the initial state of the filesystem *before* the student runs
# the required command for extracting heavy specimens.

import os
from pathlib import Path

SPECIMENS_PATH = Path("/home/user/data/specimens.tsv")
OUTPUT_DIR = Path("/home/user/output")
OUTPUT_FILE = OUTPUT_DIR / "heavy_specimens.txt"


EXPECTED_SPECIMENS_CONTENT = (
    "id\tspecies\tlocation\tweight_g\tnotes\n"
    "SPC001\tMus musculus\tLabA\t23\tpregnant\n"
    "SPC002\tRattus norvegicus\tLabB\t512\tadult\n"
    "SPC003\tMus musculus\tField\t712\tjuvenile\n"
    "SPC004\tRattus norvegicus\tLabC\t98\tadult\n"
    "SPC005\tMus musculus\tField\t501\tadult\n"
)


def test_specimens_file_exists():
    """/home/user/data/specimens.tsv must exist and be a regular readable file."""
    assert SPECIMENS_PATH.exists(), (
        f"Required source file {SPECIMENS_PATH} is missing."
    )
    assert SPECIMENS_PATH.is_file(), (
        f"{SPECIMENS_PATH} exists but is not a regular file."
    )
    # Try opening the file to confirm readability.
    try:
        with SPECIMENS_PATH.open("r", encoding="utf-8") as f:
            f.readline()
    except Exception as exc:  # pragma: no cover
        assert False, f"Cannot read {SPECIMENS_PATH}: {exc}"


def test_specimens_file_contents_exact():
    """
    /home/user/data/specimens.tsv must contain the exact expected
    tab-separated content (including newline characters).
    """
    with SPECIMENS_PATH.open("r", encoding="utf-8") as f:
        actual = f.read()

    # Compare after stripping a **single** trailing newline from both ends to be lenient
    # about the presence/absence of a final newline while still ensuring all lines match.
    actual_normalised = actual.rstrip("\n")
    expected_normalised = EXPECTED_SPECIMENS_CONTENT.rstrip("\n")

    assert (
        actual_normalised == expected_normalised
    ), (
        "The contents of /home/user/data/specimens.tsv do not match the expected "
        "fixture.\n\n"
        "Expected:\n"
        "----------\n"
        f"{EXPECTED_SPECIMENS_CONTENT}"
        "----------\n"
        "Actual:\n"
        "----------\n"
        f"{actual}\n"
        "----------"
    )


def test_output_file_absent_initially():
    """
    The heavy_specimens.txt file must NOT exist before the student's command is run.
    The directory /home/user/output/ may or may not exist, but the file itself
    must be absent so that the extraction step truly creates it.
    """
    if OUTPUT_FILE.exists():
        assert False, (
            f"Output file {OUTPUT_FILE} should not exist before the exercise begins."
        )