# test_initial_state.py
#
# This pytest file validates the initial on-disk state *before* the student
# performs any action.  It asserts that the three empty CSV stubs exist only
# inside /home/user/datasets/raw_data/ and that the processed_data directory
# is present but contains nothing.  No checks are performed on any files that
# are expected to be created by the student later on (e.g., manifest.sha256).

import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"
RAW_DIR = DATASETS_DIR / "raw_data"
PROCESSED_DIR = DATASETS_DIR / "processed_data"

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
CSV_FILES = [
    "dataset_node1.csv",
    "dataset_node2.csv",
    "dataset_node3.csv",
]


def sha256_of_file(path: Path) -> str:
    """
    Compute the SHA-256 digest (hex) of the file at *path*.

    The function streams the file to avoid loading it all at once (even though
    these CSVs are 0-byte stubs).  Using a streaming approach keeps the helper
    generally robust.
    """
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_required_directories_exist():
    """Both /home/user/datasets/raw_data/ and processed_data/ must exist."""
    assert RAW_DIR.exists(), f"Missing directory: {RAW_DIR}"
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."

    assert PROCESSED_DIR.exists(), f"Missing directory: {PROCESSED_DIR}"
    assert PROCESSED_DIR.is_dir(), f"{PROCESSED_DIR} exists but is not a directory."


@pytest.mark.parametrize("csv_name", CSV_FILES)
def test_raw_csv_files_present_and_empty(csv_name):
    """
    Each expected CSV must:

    1. Exist inside raw_data/.
    2. Be a file (not dir/symlink).
    3. Have size == 0 bytes.
    4. Have the SHA-256 of an empty file.
    """
    path = RAW_DIR / csv_name
    assert path.exists(), f"Expected CSV missing: {path}"
    assert path.is_file(), f"{path} exists but is not a regular file."

    size = path.stat().st_size
    assert size == 0, f"{path} should be 0 bytes but is {size} byte(s)."

    digest = sha256_of_file(path)
    assert (
        digest == EMPTY_SHA256
    ), f"{path} digest mismatch: expected {EMPTY_SHA256}, got {digest}"


def test_raw_dir_contains_only_expected_csvs():
    """No unexpected *.csv files should live in raw_data/."""
    csvs_on_disk = sorted(p.name for p in RAW_DIR.glob("*.csv"))
    assert (
        csvs_on_disk == CSV_FILES
    ), f"raw_data/ contains unexpected CSVs: {csvs_on_disk!r} (expected {CSV_FILES!r})"


def test_processed_dir_is_empty_before_task():
    """
    The processed_data directory should be empty at the outset: no CSVs,
    no manifest, nothing else.
    """
    contents = list(PROCESSED_DIR.iterdir())
    assert (
        not contents
    ), f"{PROCESSED_DIR} should be empty before the task, but found: {sorted(p.name for p in contents)!r}"