# test_initial_state.py
#
# Pytest suite that verifies the machine *before* the student begins the
# “Organizing Research Datasets – YAML & TOML Configuration Management” task.
#
# It asserts that the project hierarchy and all required artefacts do **not**
# exist yet.  Every assertion has a descriptive message so that, if the test
# fails, the student knows exactly what pre-existing item is causing trouble.
#
# Only Python’s standard library and pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")

# Absolute paths that must NOT exist at the start of the assignment
MISSING_DIRS = [
    HOME / "project",
    HOME / "project" / "config",
    HOME / "project" / "logs",
]

MISSING_FILES = [
    HOME / "project" / "config" / "datasets.yaml",
    HOME / "project" / "config" / "processing.toml",
    HOME / "project" / "logs"   / "config_update.log",
]


def test_home_directory_exists():
    """
    The baseline assumption for every autograder is that the user’s home
    directory is present.  If this fails, the environment is irreparably
    broken and all subsequent checks are moot.
    """
    assert HOME.exists(), f"Expected home directory {HOME} to exist."
    assert HOME.is_dir(), f"{HOME} exists but is not a directory."


@pytest.mark.parametrize("path", MISSING_DIRS)
def test_project_directories_absent(path: Path):
    """
    None of the project-related directories should exist yet.  They will be
    created by the student’s solution.
    """
    assert not path.exists(), (
        f"Directory {path} already exists. The workspace must start clean—"
        "remove it before beginning the task."
    )


@pytest.mark.parametrize("path", MISSING_FILES)
def test_project_files_absent(path: Path):
    """
    None of the specification-mandated files should be present before the
    student runs their code.
    """
    assert not path.exists(), (
        f"File {path} already exists. The task requires creating this file "
        "from scratch, so it must be absent at the outset."
    )