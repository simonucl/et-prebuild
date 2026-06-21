# test_initial_state.py
#
# This pytest test-suite validates that the required *initial* artefacts for the
# “legacy tool version audit” exercise are present **before** the student starts
# working.  Only the pre-existing files/directories are checked; nothing related
# to the expected *output* artefacts is verified, in accordance with the grading
# guidelines.

import os
import stat
import subprocess
from pathlib import Path

import pytest

# Constants for paths we need to validate.
LEGACY_DIR = Path("/home/user/legacy/bin")
LEGACY_TOOL = LEGACY_DIR / "old_tool"
EXPECTED_VERSION_LINE = "old_tool version v0.9.8-legacy"


def _assert_path_exists(path: Path, expected_type: str):
    """
    Helper that asserts the given path exists and is of the expected type
    ('file' or 'dir').  Produces a clear pytest failure message otherwise.
    """
    if not path.exists():
        pytest.fail(f"Required {expected_type} '{path}' is missing.")
    if expected_type == "dir" and not path.is_dir():
        pytest.fail(f"Expected '{path}' to be a directory but it is not.")
    if expected_type == "file" and not path.is_file():
        pytest.fail(f"Expected '{path}' to be a regular file but it is not.")


def test_legacy_directory_exists():
    """
    The directory /home/user/legacy/bin must already be present.
    """
    _assert_path_exists(LEGACY_DIR, "dir")

    # Optional: permissions check (must be readable/executable by user).
    st_mode = LEGACY_DIR.stat().st_mode
    assert bool(st_mode & stat.S_IXUSR), (
        f"Directory '{LEGACY_DIR}' exists but is not user-executable."
    )


def test_legacy_tool_exists_and_is_executable():
    """
    Validate that /home/user/legacy/bin/old_tool exists and is executable.
    """
    _assert_path_exists(LEGACY_TOOL, "file")

    # Verify executable bit.
    if not os.access(LEGACY_TOOL, os.X_OK):
        pytest.fail(f"File '{LEGACY_TOOL}' exists but is not marked executable.")


def test_legacy_tool_reports_expected_version():
    """
    Running the tool with '--version' must yield the expected single version line.
    """
    try:
        completed = subprocess.run(
            [str(LEGACY_TOOL), "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        pytest.fail(f"Executable '{LEGACY_TOOL}' could not be found.")
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Running '{LEGACY_TOOL} --version' returned non-zero exit status "
            f"{exc.returncode}.\nstdout: {exc.stdout}\nstderr: {exc.stderr}"
        )

    # stdout must contain exactly the expected version line (ignoring trailing newline).
    actual = completed.stdout.strip()
    assert (
        actual == EXPECTED_VERSION_LINE
    ), f"Version mismatch.\nExpected: {EXPECTED_VERSION_LINE!r}\nGot:      {actual!r}"