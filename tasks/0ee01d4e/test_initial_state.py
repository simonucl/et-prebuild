# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “mini artifact-tracking” exercise.  These tests are intended to run
# *before* the student executes their solution.  They guarantee that
# the workspace starts from a clean, known configuration.
#
# Rules enforced:
#   • exp_runs/ scaffold is present exactly as described.
#   • No pre-existing artifact_store/ directory or files.
#   • run_list.txt contents and newlines are exactly as specified.
#   • SHA-256 of /home/user/exp_runs/run_01/model.bin is correct
#     (empty file hash).
#   • run_02 directory exists and intentionally lacks model.bin.
#
# If any test here fails, it means the starting environment is wrong
# and the student’s work cannot be graded reliably.

import hashlib
import os
from pathlib import Path

# Absolute paths used throughout the suite
HOME = Path("/home/user")
EXP_DIR = HOME / "exp_runs"
RUN_LIST = EXP_DIR / "run_list.txt"
RUN_01_MODEL = EXP_DIR / "run_01" / "model.bin"
RUN_02_DIR = EXP_DIR / "run_02"
RUN_02_MODEL = RUN_02_DIR / "model.bin"
ARTIFACT_STORE = HOME / "artifact_store"


def test_exp_runs_directory_structure():
    """Verify that /home/user/exp_runs and its sub-items exist."""
    assert EXP_DIR.is_dir(), f"Expected directory {EXP_DIR} is missing."

    # run_list.txt must exist
    assert RUN_LIST.is_file(), f"Expected file {RUN_LIST} is missing."

    # run_01 directory and model.bin must exist
    assert RUN_01_MODEL.parent.is_dir(), (
        f"Expected directory {RUN_01_MODEL.parent} is missing."
    )
    assert RUN_01_MODEL.is_file(), (
        f"Expected model file {RUN_01_MODEL} is missing."
    )

    # run_02 directory must exist
    assert RUN_02_DIR.is_dir(), f"Expected directory {RUN_02_DIR} is missing."


def test_run_list_contents_exact():
    """
    run_list.txt must contain exactly two lines:
        run_01
        run_02
    each terminated by a newline, and *nothing* else.
    """
    expected_content = "run_01\nrun_02\n"
    actual_content = RUN_LIST.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), (
        f"{RUN_LIST} contents are not exactly as expected.\n"
        f"Expected byte sequence:\n{repr(expected_content)}\n"
        f"Actual byte sequence:\n{repr(actual_content)}"
    )


def test_run_01_model_is_empty_file_with_correct_sha256():
    """run_01/model.bin must be 0 bytes and match the empty-file SHA-256."""
    size = RUN_01_MODEL.stat().st_size
    assert size == 0, (
        f"{RUN_01_MODEL} should be empty (0 bytes) but is {size} bytes."
    )

    sha256_expected = (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    with RUN_01_MODEL.open("rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    assert (
        file_hash == sha256_expected
    ), (
        f"SHA-256 of {RUN_01_MODEL} is {file_hash}, "
        f"expected {sha256_expected}."
    )


def test_run_02_model_file_absent():
    """
    /home/user/exp_runs/run_02/ must NOT already contain model.bin.
    This missing file is required to trigger the controlled error later.
    """
    assert not RUN_02_MODEL.exists(), (
        f"{RUN_02_MODEL} should NOT exist in the initial state."
    )


def test_artifact_store_not_pre_created():
    """
    The artifact_store directory (and its contents) must not exist
    before the student runs their solution.
    """
    assert not ARTIFACT_STORE.exists(), (
        f"{ARTIFACT_STORE} should not exist yet; the student will create it."
    )