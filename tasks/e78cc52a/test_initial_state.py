# test_initial_state.py
#
# Pytest suite to validate the initial operating-system / filesystem state
# *before* the student runs any backup commands.
#
# Rules enforced:
#   • The directory /home/user/cicd/scripts must exist.
#   • The files build.sh, deploy.sh and test.sh must exist directly inside
#     that directory.
#   • Each file must contain exactly the expected two lines of text.
#
# NOTE: We deliberately do NOT test for /home/user/backups or any artefacts
# that will be produced by the student’s solution, in accordance with the
# grading-harness guidelines.

import os
from pathlib import Path

import pytest

SCRIPTS_DIR = Path("/home/user/cicd/scripts")

EXPECTED_FILES = {
    "build.sh": "#!/usr/bin/env bash\n"
                "echo \"Running build\"\n",
    "deploy.sh": "#!/usr/bin/env bash\n"
                 "echo \"Deploying application\"\n",
    "test.sh": "#!/usr/bin/env bash\n"
               "echo \"Executing tests\"\n",
}


def _read_text(path: Path) -> str:
    """
    Helper that reads a file *exactly* as UTF-8 text and ensures it ends with
    a trailing newline.  Raises with a clear message if it cannot read.
    """
    try:
        data = path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")
    return data


def test_scripts_directory_exists():
    """
    Ensure /home/user/cicd/scripts exists and is a directory.
    """
    assert SCRIPTS_DIR.exists(), (
        f"Required directory {SCRIPTS_DIR} is missing."
    )
    assert SCRIPTS_DIR.is_dir(), (
        f"{SCRIPTS_DIR} exists but is not a directory."
    )


@pytest.mark.parametrize("filename", EXPECTED_FILES.keys())
def test_each_required_script_file_exists(filename):
    """
    Validate that each required script file exists and is a regular file.
    """
    file_path = SCRIPTS_DIR / filename
    assert file_path.exists(), (
        f"Expected script {file_path} is missing."
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file."
    )


@pytest.mark.parametrize("filename, expected_content", EXPECTED_FILES.items())
def test_script_file_contents_are_correct(filename, expected_content):
    """
    Validate the exact byte-for-byte content of each script file.
    """
    file_path = SCRIPTS_DIR / filename
    # Read actual content
    actual_content = _read_text(file_path)

    # Normalise line endings: expected_content already uses '\n'
    # We compare raw strings to catch any deviation (extra spaces, lines, etc.)
    assert actual_content == expected_content, (
        f"Content of {file_path} does not match the expected template.\n"
        f"--- Expected ---\n{expected_content!r}\n"
        f"---   Found  ---\n{actual_content!r}"
    )


def test_no_extra_files_in_scripts_directory():
    """
    Ensure that no extra files are present in /home/user/cicd/scripts.
    Only the specified three script files should be there.
    """
    present_files = sorted(p.name for p in SCRIPTS_DIR.iterdir() if p.is_file())
    expected_files_sorted = sorted(EXPECTED_FILES.keys())
    assert present_files == expected_files_sorted, (
        "Unexpected file(s) found in /home/user/cicd/scripts.\n"
        f"Expected: {expected_files_sorted}\n"
        f"Found:    {present_files}"
    )