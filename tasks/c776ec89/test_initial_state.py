# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state before the student begins the task.

import os
from pathlib import Path

import pytest

# Absolute paths that must already be present.
EXP_DIR = Path("/home/user/experiments")
LOG1_PATH = EXP_DIR / "log1.txt"
LOG2_PATH = EXP_DIR / "log2.txt"

# Expected *exact* contents of the two log files, including the single
# trailing newline character at the very end of each file.
EXPECTED_LOG1_CONTENT = (
    "model_v1.ckpt\n"
    "dataset_v1.zip\n"
    "model_v1.ckpt\n"
    "metrics_v1.json\n"
    "dataset_v1.zip\n"
)

EXPECTED_LOG2_CONTENT = (
    "model_v2.ckpt\n"
    "dataset_v1.zip\n"
    "model_v1.ckpt\n"
    "metrics_v1.json\n"
    "metrics_v1.json\n"
    "model_v2.ckpt\n"
)


def _read_file(path: Path) -> str:
    """
    Utility helper that returns the full content of a text file.

    The file is opened with utf-8 encoding and no newline translation
    so that we see exactly what is on disk.
    """
    with path.open("r", encoding="utf-8", newline="") as f:
        return f.read()


def test_experiments_directory_exists():
    """The /home/user/experiments directory must exist and be a directory."""
    assert EXP_DIR.exists(), (
        f"Required directory {EXP_DIR} is missing. "
        "Create it before starting the task."
    )
    assert EXP_DIR.is_dir(), f"{EXP_DIR} exists but is not a directory."


@pytest.mark.parametrize(
    ("path", "expected_contents"),
    [
        (LOG1_PATH, EXPECTED_LOG1_CONTENT),
        (LOG2_PATH, EXPECTED_LOG2_CONTENT),
    ],
)
def test_log_files_exist_with_correct_content(path: Path, expected_contents: str):
    """
    Each required log file must exist and contain exactly the expected lines,
    including the final trailing newline character and no extra whitespace.
    """
    assert path.exists(), f"Required log file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    actual_contents = _read_file(path)

    # Compare strings directly so that any deviation (including trailing
    # whitespace or missing newlines) is caught.
    assert actual_contents == expected_contents, (
        f"Contents of {path} do not match the expected initial state.\n\n"
        f"Expected:\n{repr(expected_contents)}\n\n"
        f"Found:\n{repr(actual_contents)}\n"
        "Ensure the file has exactly the lines and trailing newline shown "
        "in the task description."
    )