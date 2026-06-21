# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state for the “optimise_app” exercise.  These tests **must** all pass
# *before* the student starts working on the task.  If any test fails it
# means the starting point of the exercise is wrong and should be fixed.
#
# IMPORTANT:  These tests purposefully check that certain files do *not*
#             yet exist; do **not** remove those assertions.

import os
import subprocess
import textwrap

import pytest

REPO_DIR = "/home/user/projects/optimize_app"
CFG_PATH = os.path.join(REPO_DIR, "solver_config.yaml")
BACKUP_PATH = os.path.join(
    REPO_DIR, "solver_config_2023-01-01T00:00:00Z.bak"
)
LOG_PATH = os.path.join(REPO_DIR, "config_changes.log")

# The expected baseline contents of solver_config.yaml *including*
# the trailing newline on the last line.
BASELINE_CONFIG = textwrap.dedent(
    """\
    solver:
      name: "glpk"
      tolerance: 1e-6
      max_iterations: 1000
      verbose: false
    """
)


def _run_git(cmd, cwd=REPO_DIR):
    """
    Helper to run a git command and capture its output.
    Raises pytest.fail on any non-zero exit code.
    Returns decoded stdout.
    """
    proc = subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        pytest.fail(
            f"Git command {' '.join(cmd)} failed with exit code "
            f"{proc.returncode}.\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout.strip()


def test_repository_exists_and_initialised():
    """The project directory must exist and be a valid Git repository."""
    assert os.path.isdir(
        REPO_DIR
    ), f"Required directory {REPO_DIR} does not exist."
    # A `.git` directory is enough to treat it as an initialised repo.
    git_dir = os.path.join(REPO_DIR, ".git")
    assert os.path.isdir(
        git_dir
    ), f"{REPO_DIR} exists but is not a Git repository (missing .git)."
    # Sanity-check that Git recognises the work-tree
    is_inside = _run_git(["rev-parse", "--is-inside-work-tree"])
    assert (
        is_inside == "true"
    ), f"{REPO_DIR} is not recognised by Git as a work tree."


def test_solver_config_yaml_baseline_contents():
    """The original solver_config.yaml must exist with the baseline content."""
    assert os.path.isfile(
        CFG_PATH
    ), f"Initial file {CFG_PATH} is missing."
    with open(CFG_PATH, "r", encoding="utf-8") as fh:
        data = fh.read()
    assert (
        data == BASELINE_CONFIG
    ), (
        f"{CFG_PATH} does not match the expected baseline content.\n"
        "If the student has already modified the file, restore the original "
        "version before running these tests."
    )


def test_no_backup_file_yet():
    """The backup file must NOT exist before the student performs the task."""
    assert not os.path.exists(
        BACKUP_PATH
    ), f"Backup file {BACKUP_PATH} should not exist yet."


def test_no_change_log_yet():
    """The change-tracking log must NOT exist yet."""
    assert not os.path.exists(
        LOG_PATH
    ), f"Change-tracking log {LOG_PATH} should not exist yet."