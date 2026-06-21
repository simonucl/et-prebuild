# test_initial_state.py
"""
Pytest suite that verifies the *initial* filesystem state for the
“requirements‐cleanup” exercise.

This test file intentionally checks ONLY the resources that should
already exist **before** the student performs any work.  It does NOT
look for the output file that the student is expected to create
(`/home/user/data/experiment/requirements_clean.txt`).

If any of the following assertions fail, the exercise’s fixture is
broken and must be fixed before the student can reasonably proceed.
"""

import os
from pathlib import Path

import pytest

# Hard-coded paths (absolute, as required)
BASE_DIR = Path("/home/user/data/experiment")
RAW_REQUIREMENTS = BASE_DIR / "requirements_raw.txt"


@pytest.fixture(scope="module")
def raw_file_content():
    """Return the full text content of requirements_raw.txt."""
    if not RAW_REQUIREMENTS.exists():
        pytest.skip(f"Expected file {RAW_REQUIREMENTS!s} is missing.")
    return RAW_REQUIREMENTS.read_text(encoding="utf-8")


def test_experiment_directory_exists():
    """The /home/user/data/experiment directory must exist."""
    assert BASE_DIR.exists(), (
        f"Directory {BASE_DIR!s} is missing. "
        "The exercise expects this directory to be present *before* any work begins."
    )
    assert BASE_DIR.is_dir(), f"{BASE_DIR!s} exists but is not a directory."


def test_raw_requirements_file_exists_and_is_regular():
    """requirements_raw.txt must exist and be a regular file."""
    assert RAW_REQUIREMENTS.exists(), (
        f"File {RAW_REQUIREMENTS!s} is missing. "
        "The initial dataset must include this file."
    )
    assert RAW_REQUIREMENTS.is_file(), (
        f"{RAW_REQUIREMENTS!s} exists but is not a regular file."
    )


def test_raw_requirements_content_exact(raw_file_content):
    """
    The raw requirements file must have exactly five lines, in the precise order
    specified by the exercise, each terminated by a single '\n'.
    """
    expected_lines = [
        "numpy==1.23.5\n",
        "pandas==1.5.3\n",
        "scipy==1.9.3\n",
        "numpy==1.23.5\n",
        "matplotlib==3.6.2\n",
    ]

    # Splitlines with keepends=True to retain newline characters for comparison.
    actual_lines = raw_file_content.splitlines(keepends=True)

    # Use assertion with a helpful diff if lines differ.
    assert (
        actual_lines == expected_lines
    ), (
        "The content of requirements_raw.txt does not match the expected initial "
        "state.\n\nEXPECTED:\n"
        + "".join(expected_lines)
        + "\nACTUAL:\n"
        + "".join(actual_lines)
    )