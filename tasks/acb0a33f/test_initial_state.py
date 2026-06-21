# test_initial_state.py
"""
Pytest suite to validate the *initial* workspace state
BEFORE the student performs any actions.

These tests assert that only the pre-existing file
`/home/user/sample.env` is present and that none of the target
directories / files required in the final state have been created yet.
"""

from pathlib import Path
import pytest
import os
import stat

HOME = Path("/home/user")
PIPELINES_DIR = HOME / "pipelines"


def _assert_not_exists(path: Path):
    """Helper that raises an assertion with a clear message if path exists."""
    assert not path.exists(), f"Path should NOT exist yet, but does: {path}"


def test_sample_env_exists_with_expected_content():
    """
    1. The seed file `/home/user/sample.env` must exist.
    2. It must be a file (not a directory, symlink, etc.).
    3. Its exact bytes must match the expected template.
    """
    sample_path = HOME / "sample.env"
    assert sample_path.exists(), "Expected seed file '/home/user/sample.env' is missing."
    assert sample_path.is_file(), "'/home/user/sample.env' exists but is not a regular file."

    expected_bytes = b"# Sample environment file\n"
    actual_bytes = sample_path.read_bytes()
    assert (
        actual_bytes == expected_bytes
    ), (
        "The contents of '/home/user/sample.env' do not match the expected initial value.\n"
        f"Expected bytes:\n{expected_bytes!r}\nActual bytes:\n{actual_bytes!r}"
    )


def test_pipeline_directories_do_not_exist_yet():
    """
    The pipelines directory tree should NOT exist before the student acts.
    This includes:
      /home/user/pipelines
      /home/user/pipelines/scripts
      /home/user/pipelines/configs
    """
    _assert_not_exists(PIPELINES_DIR)
    _assert_not_exists(PIPELINES_DIR / "scripts")
    _assert_not_exists(PIPELINES_DIR / "configs")


@pytest.mark.parametrize(
    "absent_path",
    [
        PIPELINES_DIR / "configs" / "production.env",
        PIPELINES_DIR / "scripts" / "deploy.sh",
        PIPELINES_DIR / "pipeline.log",
    ],
)
def test_target_files_are_absent(absent_path: Path):
    """
    None of the files that should be created by the student
    should exist in the initial state.
    """
    _assert_not_exists(absent_path)