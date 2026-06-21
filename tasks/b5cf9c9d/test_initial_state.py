# test_initial_state.py
"""
Pytest suite to validate the **initial** filesystem state expected by the
“name-frequency” cleaning exercise.

Rules enforced
--------------
1. The raw dataset `/home/user/datasets/raw_names.txt` **must** be present and
   readable.
2. Its byte-for-byte contents must exactly match the canonical 19-line fixture
   embedded below (including intentional casing, the three trailing spaces on
   line 6, and the single trailing newline at EOF).
3. The parent directory `/home/user/datasets` must exist and be a directory.

We purposely do *not* check anything under `/home/user/output` – presence or
absence – because the specification forbids tests that reference the output
targets before the student has created them.
"""

from pathlib import Path
import pytest

DATASET_DIR = Path("/home/user/datasets")
RAW_FILE = DATASET_DIR / "raw_names.txt"

# The canonical fixture content (19 lines + trailing newline).
_EXPECTED_LINES = [
    "Alice",
    "bob",
    "Charlie",
    "alice",
    "Bob",
    "alice   ",      # three deliberate trailing spaces
    "Alice",
    "charlie",
    "Bob",
    "Dana",
    "Eve",
    "eve",
    "Eve",
    "alice",
    "bob",
    "dana",
    "Eve",
    "Alice",
    "charlie",
]
EXPECTED_CONTENT = "\n".join(_EXPECTED_LINES) + "\n"


def test_dataset_directory_exists():
    """Ensure `/home/user/datasets` exists and is a directory."""
    assert DATASET_DIR.exists(), (
        f"Expected directory {DATASET_DIR} to exist, but it does not."
    )
    assert DATASET_DIR.is_dir(), (
        f"Expected {DATASET_DIR} to be a directory, but it is not."
    )


def test_raw_names_file_exists():
    """Ensure the raw names file exists and is a regular, readable file."""
    assert RAW_FILE.exists(), (
        f"Required file {RAW_FILE} is missing. "
        "The exercise cannot proceed without the raw data."
    )
    assert RAW_FILE.is_file(), (
        f"Expected {RAW_FILE} to be a regular file, but it is not."
    )


def test_raw_names_file_content_exact_match():
    """
    Verify that the raw names file matches the expected canonical content
    exactly (byte-for-byte, including whitespace and final newline).
    """
    try:
        raw_bytes = RAW_FILE.read_bytes()
    except Exception as exc:  # pragma: no cover  (sanity guard)
        pytest.fail(f"Could not read {RAW_FILE}: {exc}")

    # Ensure the file is valid UTF-8 and decode it
    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"{RAW_FILE} is not valid UTF-8 or contains undecodable bytes: {exc}"
        )

    assert raw_text == EXPECTED_CONTENT, (
        "The contents of /home/user/datasets/raw_names.txt do not match the "
        "expected fixture.\n"
        "Differences can include casing, leading/trailing whitespace, the exact "
        "number of spaces on line 6, or the absence/presence of the final "
        "newline. Please ensure the file is unmodified."
    )