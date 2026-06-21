# test_initial_state.py
#
# This test-suite verifies the *initial* condition of the operating-system
# before the learner starts solving the exercise.  It validates that the
# reference dataset tree is present and that no diagnostic log has yet been
# created.  If any of these assertions fail, the machine is not in the
# expected pristine state.

import os
from pathlib import Path

import pytest


DATASETS_ROOT = Path("/home/user/datasets")

# Expected relative paths and their byte sizes
EXPECTED_FILES = {
    "experiment_alpha/data1.csv": 14,
    "experiment_alpha/data2.csv": 14,
    "experiment_beta/results.json": 16,
    "experiment_beta/raw/run1.txt": 10,
}

RESEARCH_LOGS_DIR = Path("/home/user/research_logs")
LOG_GZ = RESEARCH_LOGS_DIR / "system_diagnostics.log.gz"


def _human(path: Path) -> str:
    """Return the absolute form of a Path for clearer assertion messages."""
    return str(path.resolve())


def test_datasets_directory_exists():
    """The root datasets directory must exist and be a directory."""
    assert DATASETS_ROOT.is_dir(), (
        f"Expected datasets root {_human(DATASETS_ROOT)} to exist "
        f"and be a directory, but it is missing or not a directory."
    )


@pytest.mark.parametrize("relative_path,expected_size", EXPECTED_FILES.items())
def test_expected_dataset_files_exist_and_have_correct_size(relative_path, expected_size):
    """
    Each expected file must exist, be a regular file, and have the exact size
    specified in the truth table.
    """
    file_path = DATASETS_ROOT / relative_path
    assert file_path.is_file(), (
        f"Required dataset file {_human(file_path)} is missing "
        f"or is not a regular file."
    )

    actual_size = file_path.stat().st_size
    assert actual_size == expected_size, (
        f"Dataset file {_human(file_path)} has size {actual_size} bytes, "
        f"but {expected_size} bytes were expected."
    )


def test_total_dataset_file_count_and_size():
    """
    The total number of regular files under /home/user/datasets should be 4,
    and their combined size should be 54 bytes.
    """
    all_files = [
        p
        for p in DATASETS_ROOT.rglob("*")
        if p.is_file()
    ]

    total_files = len(all_files)
    total_bytes = sum(p.stat().st_size for p in all_files)

    assert total_files == 4, (
        f"Expected exactly 4 regular files under {_human(DATASETS_ROOT)}, "
        f"but found {total_files}. The tree may have been modified."
    )
    assert total_bytes == 54, (
        f"Expected total size of all dataset files to be 54 bytes, "
        f"but calculated {total_bytes} bytes."
    )


def test_no_diagnostic_log_yet():
    """
    The compressed diagnostic log should NOT exist before the learner runs
    their solution.  Its presence would indicate that the machine is not in
    the pristine starting state.
    """
    assert not LOG_GZ.exists(), (
        f"The file {_human(LOG_GZ)} already exists, but it should be absent "
        f"at the beginning of the exercise. The learner is supposed to create "
        f"it during their solution."
    )