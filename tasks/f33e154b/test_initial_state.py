# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# filesystem before the student performs any actions for the “automatic
# data-preparation routine” task.
#
# IMPORTANT
# ---------
# • We deliberately avoid testing for *any* of the output files or
#   directories that the student is expected to create
#   (e.g. cron directory, logs directory, daily_prep.cron file, etc.).
#   The rubric explicitly forbids such checks.
# • We only verify the parts of the filesystem that must already be
#   provided to the student: the base project directory and the existing
#   data-preparation script.
#
# Expected initial state (pre-task):
#   1) Directory  /home/user/ml_training/           — must exist
#   2) Directory  /home/user/ml_training/bin/       — must exist
#   3) File       /home/user/ml_training/bin/prepare_data.sh
#      – must exist and be a regular file (optionally executable)
#
# Any deviation from these expectations will cause the tests to fail,
# providing clear, actionable messages.

import os
from pathlib import Path

# Constant paths used throughout the tests
HOME_DIR = Path("/home/user")
ML_DIR = HOME_DIR / "ml_training"
BIN_DIR = ML_DIR / "bin"
PREP_SCRIPT = BIN_DIR / "prepare_data.sh"


def _assert_path_exists(path: Path, kind: str) -> None:
    """
    Helper that asserts `path` exists and is of the given *kind*.

    Parameters
    ----------
    path : pathlib.Path
        The path to check.
    kind : str
        Either "directory" or "file".
    """
    assert path.exists(), (
        f"Required {kind} {path} is missing.\n"
        "The task must start with this path present so the student can "
        "focus solely on creating the cron schedule file."
    )
    if kind == "directory":
        assert path.is_dir(), f"Expected {path} to be a directory."
    elif kind == "file":
        assert path.is_file(), f"Expected {path} to be a regular file."
    else:
        raise ValueError(f"Invalid kind '{kind}' supplied to _assert_path_exists().")


def test_base_ml_directory_exists():
    """
    The base machine-learning directory must already exist.
    """
    _assert_path_exists(ML_DIR, "directory")


def test_bin_directory_exists():
    """
    The /home/user/ml_training/bin/ directory must already exist.
    """
    _assert_path_exists(BIN_DIR, "directory")


def test_prepare_data_script_exists():
    """
    The data-preparation script must already be present so the student
    can reference it in their cron schedule.
    """
    _assert_path_exists(PREP_SCRIPT, "file")

    # Optionally, check that the script is at least readable.
    assert os.access(PREP_SCRIPT, os.R_OK), (
        f"The script {PREP_SCRIPT} exists but is not readable. "
        "Ensure correct permissions are set."
    )