# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system state before the
# student runs the single-line command requested in the task description.
#
# What we check:
# 1. The experiment directory /home/user/experiments/quadratic_coeffs/ exists.
# 2. The coefficients file exists at the expected absolute path.
# 3. The coefficients file contains exactly one line with three real numbers
#    “2 -8 3” (whitespace-separated) and nothing else.
# 4. The artifacts directory does *not* yet exist (the student must create it).
# 5. The optimisation summary file opt_summary.json does *not* yet exist.
#
# Any deviation from the expected state will raise a clear, actionable failure
# message so that learners immediately know what is wrong *before* they attempt
# their solution.

import os
import pathlib
import re

import pytest

# Absolute paths used throughout the tests
ROOT_DIR = pathlib.Path("/home/user/experiments/quadratic_coeffs")
COEFF_FILE = ROOT_DIR / "coefficients.txt"
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
OPT_JSON = ARTIFACTS_DIR / "opt_summary.json"


def test_experiment_directory_exists():
    """The base experiment directory must already exist."""
    assert ROOT_DIR.is_dir(), (
        f"Required directory {ROOT_DIR} does not exist. "
        "Create the directory tree /home/user/experiments/quadratic_coeffs/ first."
    )


def test_coefficients_file_exists():
    """The coefficients.txt file must already be present."""
    assert COEFF_FILE.is_file(), (
        f"Expected coefficients file {COEFF_FILE} is missing. "
        "Place a file with quadratic coefficients there."
    )


def test_coefficients_file_content():
    """
    The coefficients file must contain exactly one line with the three numbers:
    2 -8 3 (whitespace-separated) and ending with a newline. No extra lines or content.
    """
    with COEFF_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert len(lines) == 1, (
        f"File {COEFF_FILE} should contain exactly one line, found {len(lines)} lines."
    )

    line = lines[0].rstrip("\n")
    # Match three floating point numbers and capture them
    match = re.fullmatch(r"\s*([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s*", line)
    assert match, (
        f"The line in {COEFF_FILE!s} must consist of three whitespace-separated numbers. "
        f"Actual content: {line!r}"
    )

    # Convert to floats and compare numerically to the truth values 2, -8, 3
    a, b, c = map(float, match.groups())
    assert (a, b, c) == (2.0, -8.0, 3.0), (
        f"Expected coefficients '2 -8 3' but found '{a:g} {b:g} {c:g}' in {COEFF_FILE}."
    )


def test_artifacts_directory_missing_initially():
    """
    The artifacts directory must *not* exist yet; the student will create it
    in their one-liner.
    """
    assert not ARTIFACTS_DIR.exists(), (
        f"Directory {ARTIFACTS_DIR} already exists, but it should be absent before running the solution."
    )


def test_opt_summary_json_absent_initially():
    """
    The output JSON must not exist before the student's command is executed.
    """
    assert not OPT_JSON.exists(), (
        f"File {OPT_JSON} already exists, but it should not be present before the student's one-liner creates it."
    )