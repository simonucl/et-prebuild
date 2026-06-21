# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the filesystem
before the learner carries out any actions.

It verifies that the raw data produced by the laboratory equipment
is already in place exactly as specified.  This provides a safety
net so that the subsequent tasks (creating links, logs, etc.) start
from a known good baseline.

IMPORTANT:  We intentionally **do not** test for the presence of any
output artefacts (e.g. */home/user/projects/datasets* or anything
inside it).  Those belong to the *result* of the exercise and will be
checked separately.
"""

from pathlib import Path

RAW_DATA_DIR = Path("/home/user/raw_data")
DATASET_A = RAW_DATA_DIR / "dataset_A_v1.csv"
DATASET_B = RAW_DATA_DIR / "dataset_B_v1.csv"

EXPECTED_CONTENT_A = "time,signal\n0,0.123\n"
EXPECTED_CONTENT_B = "time,value\n0,42.7\n"

def _read(path: Path) -> str:
    """Read file as UTF-8 text; fail loudly if it cannot be read."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        raise AssertionError(f"Could not read {path}: {exc}") from exc


def test_raw_data_directory_exists():
    assert RAW_DATA_DIR.exists(), (
        f"Expected directory {RAW_DATA_DIR} to exist, but it is missing."
    )
    assert RAW_DATA_DIR.is_dir(), (
        f"{RAW_DATA_DIR} exists but is not a directory."
    )


def test_dataset_a_exists_and_correct():
    assert DATASET_A.exists(), f"Missing expected file: {DATASET_A}"
    assert DATASET_A.is_file(), f"{DATASET_A} exists but is not a regular file."
    contents = _read(DATASET_A)
    assert contents == EXPECTED_CONTENT_A, (
        f"Contents of {DATASET_A} differ from expectations.\n"
        f"Expected:\n{EXPECTED_CONTENT_A!r}\nGot:\n{contents!r}"
    )


def test_dataset_b_exists_and_correct():
    assert DATASET_B.exists(), f"Missing expected file: {DATASET_B}"
    assert DATASET_B.is_file(), f"{DATASET_B} exists but is not a regular file."
    contents = _read(DATASET_B)
    assert contents == EXPECTED_CONTENT_B, (
        f"Contents of {DATASET_B} differ from expectations.\n"
        f"Expected:\n{EXPECTED_CONTENT_B!r}\nGot:\n{contents!r}"
    )