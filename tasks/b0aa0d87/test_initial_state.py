# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state before the
# student begins the backup-integrity exercise.
#
# Only the standard library and pytest are used.  Every assertion has a clear
# message so that a failure pin-points the missing or incorrect element.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")

SOURCE_DIR = HOME / "backup_source"
IMAGES_DIR = SOURCE_DIR / "images"
TARGET_DIR = HOME / "backup_target"

EXPECTED_SYMLINKS = {
    # basename            stored link target (exactly as it appears in the link)
    "finance_2021.csv": "../backup_source/finance_2021.csv",
    "logo.png":          "../backup_source/images/logo.png",
    "old_report.txt":    "../backup_source/reports/report_q1.txt",
}

FINANCE_CSV_CONTENT = [
    "Finance Data 2021\n",
    "ID,Amount\n",
    "1,1000\n",
]

PNG_DATA_BYTES = b"PNGDATA"


def _resolved_exists(symlink_path: Path) -> bool:
    """
    Return True if the *resolved* target of the symlink exists on disk.
    Handles both relative and absolute link targets.
    """
    stored_target = os.readlink(symlink_path)
    target_path = (
        Path(stored_target)
        if os.path.isabs(stored_target)
        else symlink_path.parent / stored_target
    )
    return target_path.exists()


@pytest.fixture(scope="module")
def target_entries():
    """
    Returns dict mapping entry name -> Path object for every item that is
    directly inside /home/user/backup_target.
    """
    assert TARGET_DIR.exists(), (
        f"Required directory missing: {TARGET_DIR!s}"
    )
    return {p.name: p for p in TARGET_DIR.iterdir()}


def test_source_directories_exist():
    assert SOURCE_DIR.is_dir(), f"Missing directory: {SOURCE_DIR}"
    assert IMAGES_DIR.is_dir(), f"Missing directory: {IMAGES_DIR}"


def test_source_files_exist_and_correct_content():
    finance_csv = SOURCE_DIR / "finance_2021.csv"
    assert finance_csv.is_file(), f"Missing file: {finance_csv}"
    with finance_csv.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()
    assert lines == FINANCE_CSV_CONTENT, (
        f"Content of {finance_csv} is incorrect. Expected exactly:\n"
        "".join(FINANCE_CSV_CONTENT)
    )

    logo_png = IMAGES_DIR / "brand_logo.png"
    assert logo_png.is_file(), f"Missing file: {logo_png}"
    with logo_png.open("rb") as fh:
        data = fh.read()
    assert data == PNG_DATA_BYTES, (
        f"Content of {logo_png} is incorrect. Expected 7 bytes 'PNGDATA'."
    )


def test_target_contains_only_expected_symlinks(target_entries):
    # 1. Exactly expected number of entries
    assert set(target_entries) == set(EXPECTED_SYMLINKS), (
        "Entries inside /home/user/backup_target/ do not match the expected "
        f"set.\nExpected: {sorted(EXPECTED_SYMLINKS)}\n"
        f"Found   : {sorted(target_entries)}"
    )

    # 2. Every entry is a symlink
    for name, path in target_entries.items():
        assert path.is_symlink(), f"{path} is expected to be a symbolic link."


def test_symlink_targets_correct(target_entries):
    for name, expected_link_target in EXPECTED_SYMLINKS.items():
        symlink_path = target_entries[name]
        stored_target = os.readlink(symlink_path)
        assert stored_target == expected_link_target, (
            f"Symlink {symlink_path} points to '{stored_target}', "
            f"but expected '{expected_link_target}'."
        )

    # Validate which links are broken or valid
    assert _resolved_exists(target_entries["finance_2021.csv"]), (
        "finance_2021.csv symlink should be VALID but its target is missing."
    )
    assert not _resolved_exists(target_entries["logo.png"]), (
        "logo.png symlink is supposed to be BROKEN but its target exists."
    )
    assert not _resolved_exists(target_entries["old_report.txt"]), (
        "old_report.txt symlink is supposed to be BROKEN but its target exists."
    )