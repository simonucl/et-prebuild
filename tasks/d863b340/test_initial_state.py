# test_initial_state.py
#
# This test-suite validates the **initial** on-disk state that must be
# present *before* the student writes their solution.  It intentionally
# does **NOT** look for any output artefacts such as
# /home/user/mlops/experiment_diagnostics.log.  Its sole purpose is to
# guarantee that the predefined experiment folders and files exist with
# the exact expected contents and sizes so that downstream grading logic
# can rely on them.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
EXP_ROOT = HOME / "mlops" / "experiments"

# --------------------------------------------------------------------------- #
# Ground-truth definition of the expected directory structure, files, content
# --------------------------------------------------------------------------- #
EXPECTED_STRUCTURE = {
    "exp_alpha": {
        "model.pt": b"alpha\n",                 # 6 bytes
        "metrics.json": b'{"accuracy":0.91}\n', # 18 bytes
        "config.yaml": b"epochs:10\n",          # 10 bytes
    },
    "exp_beta": {
        "model.pt": b"beta\n",                  # 5 bytes
        "metrics.json": b'{"accuracy":0.88}\n', # 18 bytes
        "config.yaml": b"epochs:20\n",          # 10 bytes
        "notes.txt": b"needs_tuning\n",         # 13 bytes
    },
    "exp_gamma": {
        "model.pt": b"gamma\n",                 # 6 bytes
        "metrics.json": b'{"accuracy":0.93}\n', # 18 bytes
        "config.yaml": b"epochs:15\n",          # 10 bytes
    },
}

# Pre-computed file-count & byte-totals (used by one of the tests)
EXPECTED_SUMMARIES = {
    "exp_alpha": (3, 34),
    "exp_beta": (4, 46),
    "exp_gamma": (3, 34),
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _read_bytes(path: Path) -> bytes:
    """Return file content as raw bytes, raising a helpful pytest error if it fails."""
    try:
        return path.read_bytes()
    except FileNotFoundError as exc:
        pytest.fail(f"Expected file {path} to exist but it is missing.")  # pragma: no cover
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_experiments_root_exists_and_is_directory():
    assert EXP_ROOT.exists(), f"Required directory {EXP_ROOT} does not exist."
    assert EXP_ROOT.is_dir(), f"{EXP_ROOT} exists but is not a directory."


@pytest.mark.parametrize("exp_name", sorted(EXPECTED_STRUCTURE))
def test_experiment_directories_exist(exp_name: str):
    exp_path = EXP_ROOT / exp_name
    assert exp_path.exists(), f"Experiment directory {exp_path} is missing."
    assert exp_path.is_dir(), f"{exp_path} exists but is not a directory."


@pytest.mark.parametrize(
    ("exp_name", "file_name", "expected_content"),
    [
        (exp, fname, content)
        for exp, files in EXPECTED_STRUCTURE.items()
        for fname, content in files.items()
    ],
)
def test_each_expected_file_exists_with_correct_contents(exp_name, file_name, expected_content):
    file_path = EXP_ROOT / exp_name / file_name

    # Existence & type
    assert file_path.exists(), f"Required file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    # Contents & exact byte length
    actual_bytes = _read_bytes(file_path)
    assert (
        actual_bytes == expected_content
    ), f"Content of {file_path} does not match the expected bytes."

    # Size sanity check
    expected_size = len(expected_content)
    actual_size = file_path.stat().st_size
    assert (
        actual_size == expected_size
    ), f"Size mismatch for {file_path}: expected {expected_size} bytes, found {actual_size} bytes."


@pytest.mark.parametrize("exp_name", sorted(EXPECTED_STRUCTURE))
def test_no_extra_files_in_experiment_directory(exp_name):
    """
    Ensure that *only* the expected regular files are present directly or in nested
    sub-directories of each experiment folder.  This guards against accidental
    additions that could alter byte-totals later on.
    """
    exp_path = EXP_ROOT / exp_name
    expected_files_relative = {
        Path(fname) for fname in EXPECTED_STRUCTURE[exp_name]
    }

    # Collect all regular files relative to exp_path
    actual_files_relative = {
        f.relative_to(exp_path)
        for f in exp_path.rglob("*")
        if f.is_file()
    }

    assert actual_files_relative == expected_files_relative, (
        f"Experiment {exp_name} contains unexpected files.\n"
        f"Expected files: {sorted(str(p) for p in expected_files_relative)}\n"
        f"Actual files:   {sorted(str(p) for p in actual_files_relative)}"
    )


@pytest.mark.parametrize("exp_name", sorted(EXPECTED_STRUCTURE))
def test_precomputed_totals_are_correct(exp_name):
    """
    Finally, verify that our pre-computed (file_count, byte_total) truly match the
    live filesystem.  This acts as a safety net for the grader's later assertions.
    """
    exp_path = EXP_ROOT / exp_name
    expected_count, expected_bytes = EXPECTED_SUMMARIES[exp_name]

    # Tally regular files recursively
    files = [f for f in exp_path.rglob("*") if f.is_file()]
    byte_total = sum(f.stat().st_size for f in files)

    assert len(files) == expected_count, (
        f"Internal sanity check failed for {exp_name}: "
        f"expected {expected_count} files, found {len(files)}."
    )
    assert byte_total == expected_bytes, (
        f"Internal sanity check failed for {exp_name}: "
        f"expected {expected_bytes} bytes, found {byte_total} bytes."
    )