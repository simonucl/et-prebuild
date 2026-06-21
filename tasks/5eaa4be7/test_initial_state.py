# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present before the student runs any command.  It checks that the project
# directory tree and the expected environment files (with their exact
# contents and line numbers) exist exactly as described.

import os
import pytest

# ---------------------------------------------------------------------------
# Helper data
# ---------------------------------------------------------------------------

PROJECT_ROOT = "/home/user/project"

EXPECTED_STRUCTURE = {
    "backend": {
        ".env": {
            3: 'AWS_SECRET_ACCESS_KEY="AKIA111111111EXAMPLE"',
        }
    },
    "deploy": {
        "k8s.env": {
            3: 'AWS_SECRET_ACCESS_KEY="AKIA222222222EXAMPLE"',
        }
    },
    "infra": {
        "secrets.env": {
            3: 'AWS_SECRET_ACCESS_KEY="AKIA333333333EXAMPLE"',
        }
    },
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_project_root_exists():
    """The /home/user/project directory must exist and be a directory."""
    assert os.path.isdir(PROJECT_ROOT), (
        f"Expected project root directory '{PROJECT_ROOT}' to exist."
    )


@pytest.mark.parametrize(
    "subdir",
    list(EXPECTED_STRUCTURE.keys()),
)
def test_expected_subdirectories_exist(subdir):
    """Each first-level subdirectory must exist."""
    path = os.path.join(PROJECT_ROOT, subdir)
    assert os.path.isdir(path), f"Expected directory '{path}' to exist."


@pytest.mark.parametrize(
    "relative_dir, files",
    EXPECTED_STRUCTURE.items(),
)
def test_expected_files_exist(relative_dir, files):
    """Verify that every expected file exists inside its subdirectory."""
    dir_path = os.path.join(PROJECT_ROOT, relative_dir)
    for filename in files:
        file_path = os.path.join(dir_path, filename)
        assert os.path.isfile(file_path), f"Expected file '{file_path}' to exist."


@pytest.mark.parametrize(
    "relative_dir, files",
    EXPECTED_STRUCTURE.items(),
)
def test_secret_key_lines(relative_dir, files):
    """
    For each expected file, ensure that the AWS_SECRET_ACCESS_KEY line:
      * Exists exactly once
      * Appears at the expected (1-based) line number
      * Matches the exact text
    """
    dir_path = os.path.join(PROJECT_ROOT, relative_dir)

    for filename, expected_lines in files.items():
        file_path = os.path.join(dir_path, filename)

        with open(file_path, encoding="utf-8") as fh:
            lines = [ln.rstrip("\n") for ln in fh.readlines()]

        # Check each expected line number and content
        for expected_lineno, expected_text in expected_lines.items():
            # Convert 1-based line number to list index
            idx = expected_lineno - 1
            assert idx < len(lines), (
                f"File '{file_path}' is missing line {expected_lineno}."
            )
            actual_text = lines[idx]
            assert (
                actual_text == expected_text
            ), (
                f"In file '{file_path}', line {expected_lineno} should be:\n"
                f'  {expected_text!r}\n'
                f"but found:\n"
                f'  {actual_text!r}'
            )

        # Ensure the secret appears exactly once
        secret_lines = [ln for ln in lines if "AWS_SECRET_ACCESS_KEY" in ln]
        assert len(secret_lines) == 1, (
            f"File '{file_path}' should contain exactly one "
            f"'AWS_SECRET_ACCESS_KEY' line, found {len(secret_lines)}."
        )