# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the filesystem
# before the student performs any actions described in the task.
#
# DO NOT modify this file.  If any of the following tests fail, the
# testing infrastructure will conclude that the starting conditions
# are incorrect.

import os
import shutil
import textwrap
from pathlib import Path

# --- Constants ----------------------------------------------------------------

HOME = Path("/home/user").resolve()

PROJECT_DIR = HOME / "project"
SRC_DIR = PROJECT_DIR / "src"

MAIN_FILE = SRC_DIR / "main.py"
UTILS_FILE = SRC_DIR / "utils.py"
README_FILE = PROJECT_DIR / "README.md"

# Locations that *must NOT* exist yet
ARCHIVE_DIR = HOME / "archives"
RESTORED_DIR = PROJECT_DIR / "src_restored"
LOG_DIR = HOME / "archive_logs"
ARCHIVE_FILE = ARCHIVE_DIR / "src_backup_2023.tar.gz"
LOG_FILE = LOG_DIR / "compression.log"

EXPECTED_MAIN_CONTENT = textwrap.dedent(
    """\
    # main module
    def hello():
        print("Hello from main")
    """
)

EXPECTED_UTILS_CONTENT = textwrap.dedent(
    """\
    # utility module
    def add(a, b):
        return a + b
    """
)

EXPECTED_README_CONTENT = textwrap.dedent(
    """\
    Sample project directory. Do not archive me!
    """
)

# ------------------------------------------------------------------------------


def _read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# --- Positive existence tests --------------------------------------------------


def test_project_structure_exists():
    """Verify that the initial project structure exists."""
    assert PROJECT_DIR.is_dir(), f"Missing project directory: {PROJECT_DIR}"
    assert SRC_DIR.is_dir(), f"Missing src directory: {SRC_DIR}"


def test_source_files_exist_with_expected_content_exact():
    """Both source files must exist with their exact expected content."""
    assert MAIN_FILE.is_file(), f"Missing file: {MAIN_FILE}"
    assert UTILS_FILE.is_file(), f"Missing file: {UTILS_FILE}"

    main_content = _read_text(MAIN_FILE)
    utils_content = _read_text(UTILS_FILE)

    assert (
        main_content == EXPECTED_MAIN_CONTENT
    ), f"Content of {MAIN_FILE} does not match the expected initial state."

    assert (
        utils_content == EXPECTED_UTILS_CONTENT
    ), f"Content of {UTILS_FILE} does not match the expected initial state."


def test_readme_exists_with_expected_content():
    """README.md must exist and be untouched."""
    assert README_FILE.is_file(), f"Missing README file: {README_FILE}"
    readme_content = _read_text(README_FILE)
    assert (
        readme_content == EXPECTED_README_CONTENT
    ), f"Content of {README_FILE} does not match expected."


def test_tar_is_available():
    """GNU tar must be available on the system for the student to use."""
    assert (
        shutil.which("tar") is not None
    ), "GNU tar is not installed or not found in PATH."


# --- Negative existence tests --------------------------------------------------


def test_output_directories_do_not_yet_exist():
    """Output directories should NOT exist before the student runs their solution."""
    assert (
        not ARCHIVE_DIR.exists()
    ), f"{ARCHIVE_DIR} already exists; it should be created by the student's script."
    assert (
        not LOG_DIR.exists()
    ), f"{LOG_DIR} already exists; it should be created by the student's script."
    assert (
        not RESTORED_DIR.exists()
    ), f"{RESTORED_DIR} already exists; it should be created by the student's script."


def test_output_files_do_not_yet_exist():
    """Output files should NOT exist before the student runs their solution."""
    assert (
        not ARCHIVE_FILE.exists()
    ), f"{ARCHIVE_FILE} already exists; it should be created by the student's script."
    assert (
        not LOG_FILE.exists()
    ), f"{LOG_FILE} already exists; it should be created by the student's script."