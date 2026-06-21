# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the operating system /
# filesystem before the student performs any actions.  It checks that the
# small configuration repository already exists and that
# /home/user/ci/pipeline.yml contains exactly the three expected lines
# *without* the new dependency that the student will later add.

import pathlib
import pytest


CI_DIR = pathlib.Path("/home/user/ci")
PIPELINE_FILE = CI_DIR / "pipeline.yml"


def test_ci_directory_exists():
    """
    The configuration repository directory /home/user/ci must already exist.
    """
    assert CI_DIR.is_dir(), (
        "Expected directory /home/user/ci to exist, but it was not found."
    )


def test_pipeline_yaml_initial_contents():
    """
    The initial pipeline.yml file must exist and contain exactly the three
    lines specified in the task description *before* the student makes any
    modifications.
    """
    assert PIPELINE_FILE.is_file(), (
        "Expected file /home/user/ci/pipeline.yml to exist, but it was not found."
    )

    # Read the file and split into lines without retaining newline characters.
    actual_lines = PIPELINE_FILE.read_text().splitlines()

    expected_lines = [
        "version: 1",
        "python_packages:",
        "  - pytest==7.1.2",
    ]

    assert actual_lines == expected_lines, (
        "The initial contents of /home/user/ci/pipeline.yml are not as expected.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Actual lines:\n{actual_lines}"
    )