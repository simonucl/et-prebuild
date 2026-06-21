# test_initial_state.py
"""
Pytest suite that validates the **initial** workspace state *before* the student
writes any code or runs any commands.

Assumptions taken from the task description and truth statement:
1. The experiments folder exists with exactly two sub-directories:
      /home/user/experiments/exp_alpha
      /home/user/experiments/exp_beta
2. Each of those sub-directories contains **exactly one** *.pkl* file.
   Their expected names and sizes are:
      exp_alpha/model_alpha.pkl … 19  bytes
      exp_beta/model_beta.pkl   … 34  bytes
3. Neither the tracking script nor the summary log exist yet:
      /home/user/track_artifacts.sh
      /home/user/artifacts_summary.log

If any of these pre-conditions are violated, the tests will fail with an
explanatory message so that the student (or the test harness) knows what is
missing or unexpected.
"""

import os
from pathlib import Path

EXPERIMENTS_ROOT = Path("/home/user/experiments")
EXPECTED_SUBDIRS = {
    "exp_alpha": {
        "filename": "model_alpha.pkl",
        "size": 19,
    },
    "exp_beta": {
        "filename": "model_beta.pkl",
        "size": 34,
    },
}

SCRIPT_PATH = Path("/home/user/track_artifacts.sh")
LOG_PATH = Path("/home/user/artifacts_summary.log")


def test_experiments_root_exists():
    assert EXPERIMENTS_ROOT.exists(), f"Expected directory {EXPERIMENTS_ROOT} is missing."
    assert EXPERIMENTS_ROOT.is_dir(), f"{EXPERIMENTS_ROOT} exists but is not a directory."


def test_expected_subdirectories_present_and_only_those_two_exist():
    """
    Check that the required sub-directories are present under /home/user/experiments
    and that no other unexpected experiment directories exist.
    """
    existing_dirs = sorted(
        d.name for d in EXPERIMENTS_ROOT.iterdir() if d.is_dir()
    )
    expected_dirs = sorted(EXPECTED_SUBDIRS.keys())

    # Ensure presence
    for sub in expected_dirs:
        assert sub in existing_dirs, (
            f"Missing expected sub-directory {sub} inside {EXPERIMENTS_ROOT}."
        )

    # Ensure no extras
    extra_dirs = [d for d in existing_dirs if d not in expected_dirs]
    assert not extra_dirs, (
        f"Found unexpected experiment directories inside {EXPERIMENTS_ROOT}: {extra_dirs}"
    )


def test_each_subdir_has_single_expected_pkl_with_correct_size_and_content():
    """
    For each experiment sub-directory:
      * exactly one *.pkl* file present
      * filename matches the expected name
      * file size in bytes matches the expected size
    """
    for subdir_name, meta in EXPECTED_SUBDIRS.items():
        subdir_path = EXPERIMENTS_ROOT / subdir_name
        assert subdir_path.is_dir(), f"{subdir_path} should be a directory."

        pkl_files = list(subdir_path.glob("*.pkl"))
        assert len(pkl_files) == 1, (
            f"{subdir_path} must contain exactly one .pkl file, "
            f"found {len(pkl_files)}: {[p.name for p in pkl_files]}"
        )

        pkl_path = pkl_files[0]

        # Check filename
        expected_name = meta["filename"]
        assert pkl_path.name == expected_name, (
            f"Unexpected pickle filename in {subdir_path}. "
            f"Expected '{expected_name}', found '{pkl_path.name}'."
        )

        # Check size
        expected_size = meta["size"]
        actual_size = pkl_path.stat().st_size
        assert actual_size == expected_size, (
            f"Size mismatch for {pkl_path}: expected {expected_size} bytes, "
            f"found {actual_size} bytes."
        )


def test_script_and_log_do_not_exist_yet():
    assert not SCRIPT_PATH.exists(), (
        f"{SCRIPT_PATH} should not exist before the student creates it."
    )
    assert not LOG_PATH.exists(), (
        f"{LOG_PATH} should not exist before the student runs the script."
    )