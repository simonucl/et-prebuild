# test_initial_state.py
#
# This pytest suite verifies the **initial** filesystem state
# before the student reorganises /home/user/dev_project.
#
# It asserts that:
#   1. The four loose files are present directly in the project root.
#   2. The three target sub-directories (src, docs, tests) do **not** yet exist.
#   3. The FILE_MANIFEST.txt file does **not** yet exist.
#
# If any assertion fails, the accompanying message pin-points exactly
# what is wrong so the learner knows what they must fix.

from pathlib import Path
import pytest

PROJECT_ROOT = Path("/home/user/dev_project").expanduser()

REQUIRED_FILES = [
    PROJECT_ROOT / "app.py",
    PROJECT_ROOT / "test_app.py",
    PROJECT_ROOT / "README.txt",
    PROJECT_ROOT / "changelog.md",
]

DISALLOWED_PATHS = {
    "directory": [
        PROJECT_ROOT / "src",
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "tests",
    ],
    "file": [
        PROJECT_ROOT / "FILE_MANIFEST.txt",
    ],
}


def test_project_root_exists_and_is_directory():
    assert PROJECT_ROOT.exists(), f"Expected project root {PROJECT_ROOT} to exist."
    assert PROJECT_ROOT.is_dir(), f"{PROJECT_ROOT} exists but is not a directory."


@pytest.mark.parametrize("file_path", REQUIRED_FILES)
def test_required_files_are_present_in_root(file_path: Path):
    assert file_path.exists(), (
        f"Required file {file_path} is missing.\n"
        "The project should begin with four loose files in the root directory:\n"
        "  - app.py\n  - test_app.py\n  - README.txt\n  - changelog.md"
    )
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."


@pytest.mark.parametrize("path", DISALLOWED_PATHS["directory"])
def test_target_directories_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"Directory {path} should NOT exist yet.\n"
        "It must be created by the student during the re-organisation step."
    )


@pytest.mark.parametrize("path", DISALLOWED_PATHS["file"])
def test_manifest_file_does_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"Manifest {path} should NOT exist before the re-organisation task is performed."
    )