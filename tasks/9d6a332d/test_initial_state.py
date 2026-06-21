# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state
# matches the specification *before* the student performs any action.
#
# What must already exist:
#   • /home/user/observability                          (directory)
#   • /home/user/observability/dashboards               (directory)
#   • /home/user/observability/dashboards/archive       (directory)
#   • /home/user/observability/dashboards/archive/2023  (directory)
#   • /home/user/observability/dashboards/archive/2023/performance_dashboard.json  (file)
#
# What must *not* exist yet (these will be created by the student):
#   • /home/user/observability/dashboards/old_templates      (symlink)
#   • /home/user/observability/verification.log              (file)
#
# Any deviation from this baseline should produce a clear, actionable
# failure message.

import os
from pathlib import Path

import pytest

# Base paths
HOME = Path("/home/user")
OBSERVABILITY = HOME / "observability"
DASHBOARDS = OBSERVABILITY / "dashboards"
ARCHIVE = DASHBOARDS / "archive"
YEAR2023 = ARCHIVE / "2023"
PERFORMANCE_DASH = YEAR2023 / "performance_dashboard.json"
SYMLINK_PATH = DASHBOARDS / "old_templates"
VERIFICATION_LOG = OBSERVABILITY / "verification.log"


@pytest.mark.parametrize(
    "path, expected_type, description",
    [
        (OBSERVABILITY, "dir", "observability directory"),
        (DASHBOARDS, "dir", "dashboards directory"),
        (ARCHIVE, "dir", "archive directory"),
        (YEAR2023, "dir", "2023 archive directory"),
        (PERFORMANCE_DASH, "file", "performance_dashboard.json file"),
    ],
)
def test_preexisting_items(path: Path, expected_type: str, description: str):
    """
    Ensure that all required directories and files are present
    before the student starts modifying the filesystem.
    """
    assert path.exists(), f"Missing {description}: expected at {path}"

    if expected_type == "dir":
        assert path.is_dir(), (
            f"{description} exists at {path} but is not a directory."
        )
    elif expected_type == "file":
        assert path.is_file(), (
            f"{description} exists at {path} but is not a file."
        )
    else:
        pytest.fail(f"Test mis-configuration: unknown expected_type '{expected_type}'.")


@pytest.mark.parametrize(
    "path, description",
    [
        (SYMLINK_PATH, "old_templates symlink"),
        (VERIFICATION_LOG, "verification.log file"),
    ],
)
def test_items_not_yet_present(path: Path, description: str):
    """
    Confirm that artefacts the student is supposed to create
    do NOT exist yet.  Their presence would indicate that the
    environment is not in its pristine state.
    """
    assert not path.exists(), (
        f"{description} already exists at {path}, "
        "but it should be created by the student during the exercise."
    )


def test_symlink_path_is_free_of_partial_components():
    """
    Guard against cases where something exists at the parent path that would
    block creation of the required symlink. For instance, if a regular file
    named 'old_templates' exists already, the student cannot create the symlink.
    """
    if SYMLINK_PATH.exists():
        pytest.fail(
            f"A filesystem object already exists at {SYMLINK_PATH!s}. "
            "It must be absent so the student can create the symbolic link."
        )

    # Additionally ensure no broken symlink lingers (is_symlink() is True even if broken)
    if SYMLINK_PATH.is_symlink():
        pytest.fail(
            f"A dangling symlink is present at {SYMLINK_PATH!s}. "
            "Remove it to restore the clean initial state."
        )