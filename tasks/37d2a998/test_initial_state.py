# test_initial_state.py
#
# This pytest suite validates that the sandbox **before** the student
# starts solving the exercise contains the exact directory layout and
# file contents required by the specification.  If any of these tests
# fail, the environment is not in the expected initial state and the
# exercise itself would be impossible to solve as described.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()
RELEASES_DIR = HOME / "releases"
DEPLOYMENTS_DIR = HOME / "deployments"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_text(path: Path) -> str:
    """Return the full text of *path* (utf-8) or raise an AssertionError
    with a clear message if something goes wrong.
    """
    assert path.exists(), f"Expected file '{path}' to exist."
    assert path.is_file(), f"Expected '{path}' to be a regular file."
    try:
        data = path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read '{path}': {exc}")
    return data


# ---------------------------------------------------------------------------
# Tests for the releases tree
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "release_folder,expected_content",
    [
        (
            "release_2023-09-01",
            "BUILD_ID: 202309011230\n"
            "VERSION: v1.4.2\n"
            "COMMIT: 1a2b3c4d\n",
        ),
        (
            "release_2023-09-08",
            "BUILD_ID: 202309081305\n"
            "VERSION: v1.5.0\n"
            "COMMIT: 5d6e7f8g\n",
        ),
    ],
)
def test_build_info_files_exist_with_exact_contents(release_folder, expected_content):
    """
    For every known release directory we expect an accompanying build.info file
    whose *entire* contents must match exactly what the task description
    specifies (including the trailing newline).
    """
    rel_dir = RELEASES_DIR / release_folder
    assert rel_dir.exists() and rel_dir.is_dir(), (
        f"Release directory '{rel_dir}' is missing. "
        "The exercise expects this directory to exist before students start."
    )

    build_info_path = rel_dir / "build.info"
    actual = read_text(build_info_path)

    assert (
        actual == expected_content
    ), f"Contents of '{build_info_path}' do not match the expected initial state."


def test_no_extra_release_directories_present():
    """
    The initial state must contain *only* the two release directories mentioned
    in the task description—nothing more, nothing less.
    """
    expected_dirs = {"release_2023-09-01", "release_2023-09-08"}
    actual_dirs = {p.name for p in RELEASES_DIR.iterdir() if p.is_dir()}
    missing = expected_dirs - actual_dirs
    extra = actual_dirs - expected_dirs
    assert not missing, f"Missing release directories: {', '.join(sorted(missing))}"
    assert not extra, f"Unexpected extra release directories: {', '.join(sorted(extra))}"


# ---------------------------------------------------------------------------
# Tests for the deployments tree
# ---------------------------------------------------------------------------


def test_deployment_status_log_exists_and_has_exact_contents():
    """
    Validate that /home/user/deployments/deployment_status.log exists and that
    its contents match the specification *exactly* (including trailing
    newline).
    """
    expected_log = (
        "[2023-09-01 12:30] release_2023-09-01: SUCCESS\n"
        "[2023-09-01 12:45] release_2023-09-01: DEPLOYED\n"
        "[2023-09-08 13:15] release_2023-09-08: FAILED\n"
        "[2023-09-08 13:40] release_2023-09-08: ROLLBACK_COMPLETED\n"
    )
    log_path = DEPLOYMENTS_DIR / "deployment_status.log"
    actual_log = read_text(log_path)
    assert (
        actual_log == expected_log
    ), f"Contents of '{log_path}' do not match the expected initial state."


def test_no_output_files_exist_yet():
    """
    Ensure that the files students are supposed to create during the exercise
    are *not* present in the initial state.
    """
    output_paths = [
        RELEASES_DIR / "release_versions.csv",
        DEPLOYMENTS_DIR / "failed_deployments.log",
    ]
    for path in output_paths:
        assert not path.exists(), (
            f"Output file '{path}' should not exist before the student starts "
            "working on the exercise."
        )