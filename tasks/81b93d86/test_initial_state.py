# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student begins the exercise.  These checks guarantee that
# the playground starts from the exact, known baseline described in the
# task description.
#
# Rules respected:
#   • Full, absolute paths are used everywhere.
#   • Only the Python standard library + pytest are imported.
#   • Assertions contain clear, actionable failure messages.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
EXP_DIR = HOME / "experiments"

# --------------------------------------------------------------------------- #
# Static expectation tables (path → expected byte size)
# --------------------------------------------------------------------------- #
_EXPECTED_FILES_AND_SIZES = {
    # run_2023-08-01
    "/home/user/experiments/run_2023-08-01/logs/train.log": 20,
    "/home/user/experiments/run_2023-08-01/logs/val.log": 18,
    "/home/user/experiments/run_2023-08-01/metrics.json": 34,
    "/home/user/experiments/run_2023-08-01/model_epoch=01.ckpt": 5,
    "/home/user/experiments/run_2023-08-01/model_epoch=02.ckpt": 5,
    # run_2023-08-02
    "/home/user/experiments/run_2023-08-02/logs/train.log": 20,
    "/home/user/experiments/run_2023-08-02/logs/val.log": 18,
    "/home/user/experiments/run_2023-08-02/metrics.json": 34,
    "/home/user/experiments/run_2023-08-02/model_epoch=03.ckpt": 5,
    "/home/user/experiments/run_2023-08-02/model_epoch=04.ckpt": 5,
    # run_2023-08-03
    "/home/user/experiments/run_2023-08-03/logs/train.log": 20,
    "/home/user/experiments/run_2023-08-03/logs/val.log": 18,
}

_EXPECTED_CKPT_FILES = {
    "/home/user/experiments/run_2023-08-01/model_epoch=01.ckpt",
    "/home/user/experiments/run_2023-08-01/model_epoch=02.ckpt",
    "/home/user/experiments/run_2023-08-02/model_epoch=03.ckpt",
    "/home/user/experiments/run_2023-08-02/model_epoch=04.ckpt",
}

_RUN_DIRS = {
    "/home/user/experiments/run_2023-08-01",
    "/home/user/experiments/run_2023-08-02",
    "/home/user/experiments/run_2023-08-03",
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def as_path(obj) -> Path:
    """Cast to pathlib.Path."""
    if isinstance(obj, Path):
        return obj
    return Path(obj)

def file_size(path: str | Path) -> int:
    """Return the size of *path* in bytes."""
    return as_path(path).stat().st_size

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_base_experiments_directory_exists():
    assert EXP_DIR.is_dir(), f"Expected base directory '{EXP_DIR}' to exist."

def test_ckpt_archive_does_not_exist_yet():
    ckpt_archive = EXP_DIR / "ckpt_archive"
    assert not ckpt_archive.exists(), (
        f"Checkpoint archive '{ckpt_archive}' should NOT exist before the "
        "student runs their solution."
    )

@pytest.mark.parametrize("run_dir", sorted(_RUN_DIRS))
def test_run_directories_exist(run_dir):
    run_dir_path = Path(run_dir)
    assert run_dir_path.is_dir(), f"Expected run directory '{run_dir}' to exist."

@pytest.mark.parametrize("file_path,expected_size", sorted(_EXPECTED_FILES_AND_SIZES.items()))
def test_expected_files_present_with_correct_size(file_path, expected_size):
    p = Path(file_path)
    assert p.is_file(), f"Expected file '{file_path}' to exist."
    actual_size = file_size(p)
    assert actual_size == expected_size, (
        f"File '{file_path}' expected to be {expected_size} bytes but is "
        f"{actual_size} bytes."
    )

def test_ckpt_files_only_in_first_two_runs():
    """All .ckpt files must reside in run_2023-08-01/02; run_2023-08-03 should have none."""
    all_ckpts = {str(p) for p in EXP_DIR.rglob("*.ckpt")}
    # 1. The set of ckpt files must match the expected list exactly
    assert all_ckpts == _EXPECTED_CKPT_FILES, (
        "Mismatch in checkpoint (.ckpt) files detected.\n"
        f"Expected: {sorted(_EXPECTED_CKPT_FILES)}\n"
        f"Found   : {sorted(all_ckpts)}"
    )
    # 2. Confirm run_2023-08-03 has zero ckpt files
    run3_ckpts = list((EXP_DIR / "run_2023-08-03").rglob("*.ckpt"))
    assert not run3_ckpts, (
        "run_2023-08-03 is expected to have NO checkpoint files, "
        f"but found: {run3_ckpts}"
    )

def test_total_number_of_ckpt_files_is_four():
    ckpts_found = list(EXP_DIR.rglob("*.ckpt"))
    assert len(ckpts_found) == 4, (
        f"Expected exactly 4 checkpoint files before the move, "
        f"but found {len(ckpts_found)}: {ckpts_found}"
    )

def test_output_artifacts_absent_before_student_runs_solution():
    inventory = EXP_DIR / "artifact_inventory.csv"
    cleanup = EXP_DIR / "cleanup.log"

    assert not inventory.exists(), (
        f"Inventory file '{inventory}' must NOT exist before the student runs "
        "their solution."
    )
    assert not cleanup.exists(), (
        f"Cleanup log '{cleanup}' must NOT exist before the student runs "
        "their solution."
    )