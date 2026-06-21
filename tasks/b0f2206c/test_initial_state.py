# test_initial_state.py
#
# Pytest suite to validate the *initial* filesystem state _before_
# the student’s provisioning script runs.  These tests enforce the
# assumptions laid out in the task description so that any pre-existing
# artefacts will be caught early and reported with clear messages.
#
# NOTE: Do **not** modify this file; it is evaluated by an automated
# grader.  All checks are intentionally negative (i.e. they assert the
# absence of files/directories that the student is expected to create).

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
DEPLOYMENTS = HOME / "deployments"


def test_deployments_directory_exists_and_is_empty():
    """/home/user/deployments must exist and be completely empty."""
    assert DEPLOYMENTS.exists(), (
        f"Expected directory {DEPLOYMENTS} to exist, "
        "but it is missing."
    )
    assert DEPLOYMENTS.is_dir(), (
        f"{DEPLOYMENTS} exists but is not a directory."
    )

    contents = list(DEPLOYMENTS.iterdir())
    assert (
        len(contents) == 0
    ), (
        f"{DEPLOYMENTS} must be empty before the student runs any code.\n"
        f"Found unexpected entries: {[p.name for p in contents]}"
    )


def test_envs_directory_not_present_yet():
    """The envs/ directory must not exist prior to the student's action."""
    envs_dir = DEPLOYMENTS / "envs"
    assert (
        not envs_dir.exists()
    ), f"Directory {envs_dir} should NOT exist yet."


def test_current_env_symlink_not_present():
    """current.env symlink must not exist initially."""
    current_env = DEPLOYMENTS / "current.env"
    assert (
        not current_env.exists()
    ), f"{current_env} should not be present before provisioning."


def test_logs_directory_not_present_yet():
    """logs/ directory must not exist prior to the student's action."""
    logs_dir = DEPLOYMENTS / "logs"
    assert (
        not logs_dir.exists()
    ), f"Directory {logs_dir} should NOT exist yet."


def test_bashrc_exists_and_has_no_source_line():
    """
    /home/user/.bashrc must exist but must NOT yet contain the
    'source /home/user/deployments/current.env' line.
    """
    bashrc = HOME / ".bashrc"
    assert bashrc.exists(), f"Expected file {bashrc} to exist."
    assert bashrc.is_file(), f"{bashrc} exists but is not a regular file."

    content = bashrc.read_text(encoding="utf-8", errors="ignore").splitlines()
    forbidden_line = "source /home/user/deployments/current.env"
    assert all(
        line.strip() != forbidden_line for line in content
    ), (
        f"The line '{forbidden_line}' should NOT be present in the initial "
        ".bashrc.  It must only be appended by the student's solution, and "
        "only once."
    )