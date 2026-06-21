# test_initial_state.py
#
# This pytest suite verifies that the filesystem starts in the correct,
# untouched state before the student runs any command.  If any assertion
# fails, the accompanying message will tell the student exactly what is
# missing or incorrect.
#
# Requirements verified:
#   1. /home/user/datasets/ directory exists with 0755 permissions.
#   2. /home/user/datasets/sugar_levels.csv exists, has 0644 permissions,
#      and its bytes match the expected “duplicate-containing” text.
#   3. /home/user/datasets/sugar_levels_dedup.csv must NOT exist yet.
#
# Only stdlib + pytest are used, in accordance with the instructions.

import os
from pathlib import Path
import stat
import pytest

DATASETS_DIR = Path("/home/user/datasets")
ORIGINAL_FILE = DATASETS_DIR / "sugar_levels.csv"
DEDUP_FILE = DATASETS_DIR / "sugar_levels_dedup.csv"

# Expected original file contents (INCLUDING the final newline character).
EXPECTED_ORIGINAL_CONTENT = (
    "patient_id,glucose_mg_dl,timestamp\n"
    "P001,110,2023-07-01 09:00\n"
    "P002,145,2023-07-01 09:05\n"
    "P001,110,2023-07-01 09:00\n"
    "P003,90,2023-07-01 09:10\n"
    "P002,145,2023-07-01 09:05\n"
    "P004,130,2023-07-01 09:15\n"
)

def _perm_bits(path: Path) -> int:
    """Return the rwxrwxrwx permission bits of a Path as an int (e.g. 0o755)."""
    return stat.S_IMODE(path.stat().st_mode)

@pytest.mark.order(1)
def test_datasets_directory_exists_and_permissions():
    assert DATASETS_DIR.exists(), (
        f"Required directory {DATASETS_DIR} is missing."
    )
    assert DATASETS_DIR.is_dir(), (
        f"{DATASETS_DIR} exists but is not a directory."
    )
    expected_perm = 0o755
    actual_perm = _perm_bits(DATASETS_DIR)
    assert actual_perm == expected_perm, (
        f"{DATASETS_DIR} should have permissions 0o755; found {oct(actual_perm)}."
    )

@pytest.mark.order(2)
def test_original_csv_exists_permissions_and_content():
    assert ORIGINAL_FILE.exists(), (
        f"Original CSV {ORIGINAL_FILE} is missing."
    )
    assert ORIGINAL_FILE.is_file(), (
        f"{ORIGINAL_FILE} exists but is not a regular file."
    )

    expected_perm = 0o644
    actual_perm = _perm_bits(ORIGINAL_FILE)
    assert actual_perm == expected_perm, (
        f"{ORIGINAL_FILE} should have permissions 0o644; found {oct(actual_perm)}."
    )

    with ORIGINAL_FILE.open("r", encoding="utf-8") as fp:
        content = fp.read()

    assert content == EXPECTED_ORIGINAL_CONTENT, (
        f"Contents of {ORIGINAL_FILE} do not match the expected initial text.\n\n"
        "If you have already modified this file, restore it to the exact original "
        "state before proceeding."
    )

@pytest.mark.order(3)
def test_dedup_file_not_present_yet():
    assert not DEDUP_FILE.exists(), (
        f"{DEDUP_FILE} should NOT exist yet. "
        "Create it only after running your single-line deduplication command."
    )