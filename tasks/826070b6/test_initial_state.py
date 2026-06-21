# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# before the student writes any solution code.  It checks that
# the Maven build log is present and correct and confirms that
# the target output directory / files do **not** yet exist.
#
# The tests purposefully **fail fast** with clear error messages
# so that any deviation from the expected starting point is
# obvious to the learner and the autograder alike.
#
# Only the Python standard library and pytest are used.

import os
import re
from pathlib import Path

import pytest

HOME = Path("/home/user")

INPUT_DIR = HOME / "build_logs"
INPUT_FILE = INPUT_DIR / "full_build.log"

OUTPUT_DIR = HOME / "artifact_reports"
OUTPUT_FILE = OUTPUT_DIR / "20240123_artifacts.log"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_input_file() -> list[str]:
    """
    Read the input log file and return its lines with trailing newlines
    stripped for easier comparison.
    """
    with INPUT_FILE.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_input_directory_exists():
    """The /home/user/build_logs directory must exist."""
    assert INPUT_DIR.exists(), (
        f"Required directory missing: {INPUT_DIR}"
    )
    assert INPUT_DIR.is_dir(), (
        f"Expected a directory at {INPUT_DIR}, but found something else."
    )


def test_input_log_exists_and_is_file():
    """The verbose Maven build log must be present and a regular file."""
    assert INPUT_FILE.exists(), (
        f"Required input log file missing: {INPUT_FILE}"
    )
    assert INPUT_FILE.is_file(), (
        f"Expected {INPUT_FILE} to be a regular file."
    )
    # Sanity-check that the file is not empty
    assert INPUT_FILE.stat().st_size > 0, (
        f"The input log file {INPUT_FILE} is unexpectedly empty."
    )


def test_input_log_contains_expected_artifact_lines():
    """
    The build log must contain exactly the three expected “Artifact:” lines
    from the task description (order matters).
    """
    expected_lines = [
        "2024-01-23 10:15:35,456 [INFO] Artifact: commons-lang3-3.12.0.jar SHA256=aae3fc61d7",
        "2024-01-23 10:15:36,001 [INFO] Artifact: guava-32.0.1.jar SHA256=bbeef1023a",
        "2024-01-23 10:15:38,789 [INFO] Artifact: my-app-1.2.1-SNAPSHOT.jar SHA256=caa12cc998",
    ]

    lines = _read_input_file()

    # Filter only the lines containing the literal text "Artifact:"
    artifact_lines = [ln for ln in lines if "Artifact:" in ln]

    assert artifact_lines, (
        "No lines containing the literal text 'Artifact:' were found "
        f"in {INPUT_FILE}. The file is not the expected build log."
    )

    assert artifact_lines == expected_lines, (
        "The 'Artifact:' lines in the input log do not match the expected "
        "reference lines.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        + "\n".join(expected_lines)
        + "\n\nFound ({len(artifact_lines)} lines):\n"
        + "\n".join(artifact_lines)
    )

    # Additionally assert that there are exactly 3 artifact lines.
    assert len(artifact_lines) == 3, (
        f"Expected exactly 3 'Artifact:' lines in the log, "
        f"but found {len(artifact_lines)}."
    )


def test_output_directory_absent_initially():
    """
    The /home/user/artifact_reports directory must NOT exist yet.
    It is the student's responsibility to create it.
    """
    assert not OUTPUT_DIR.exists(), (
        f"The directory {OUTPUT_DIR} already exists, "
        "but it should be created by the student's solution."
    )


def test_output_file_absent_initially():
    """
    The final report file must NOT exist before the student runs their
    commands.  Its presence would indicate that the environment is dirty.
    """
    assert not OUTPUT_FILE.exists(), (
        f"The file {OUTPUT_FILE} already exists, "
        "but it should only be produced by the student's solution."
    )