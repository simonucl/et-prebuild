# test_initial_state.py
#
# This test-suite validates the operating-system state **before** the student
# carries out any work.  It confirms that the source files/directories that must
# be archived are present and that the destination backup location has NOT yet
# been created.

from pathlib import Path
import textwrap

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state of the filesystem.
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")

SRC_DIR = HOME / "projects" / "test_env"
SRC_FILES = {
    SRC_DIR / "config.yaml": textwrap.dedent(
        """\
        env: staging
        version: 1.0
        """
    ).rstrip("\n"),
    SRC_DIR / "test_data.csv": textwrap.dedent(
        """\
        id,value
        1,foo
        2,bar
        """
    ).rstrip("\n"),
    SRC_DIR / "readme.md": textwrap.dedent(
        """\
        # Test Environment
        This directory contains configuration and data for QA tests.
        """
    ).rstrip("\n"),
}

BACKUP_DIR = HOME / "backups"
ARCHIVE_PATH = BACKUP_DIR / "test_env_backup.tar.gz"
LOG_PATH = BACKUP_DIR / "backup_log.txt"


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_source_directory_exists():
    assert SRC_DIR.is_dir(), (
        f"Required directory {SRC_DIR} is missing. "
        "It should contain the files to be archived."
    )


def test_all_source_files_exist_with_exact_content():
    """
    Each expected source file must exist and its content must match the
    reference text exactly (ignoring a trailing newline, which Git or editors
    may or may not add).
    """
    for file_path, expected_content in SRC_FILES.items():
        assert file_path.is_file(), f"Missing required file: {file_path}"
        actual_content = file_path.read_text().rstrip("\n")
        assert (
            actual_content == expected_content
        ), f"Content mismatch in {file_path}. Expected:\n{expected_content!r}\nGot:\n{actual_content!r}"


def test_backup_directory_does_not_yet_exist():
    """
    The backup destination directory should NOT exist before the student
    executes their solution.  Its creation is one of the required steps.
    """
    assert not BACKUP_DIR.exists(), (
        f"The backup directory {BACKUP_DIR} already exists, but the "
        "instructions state that it should not be present initially."
    )


def test_archive_and_log_do_not_yet_exist():
    """
    Neither the archive nor the log file should exist before the student
    performs the backup.
    """
    assert not ARCHIVE_PATH.exists(), (
        f"Archive {ARCHIVE_PATH} already exists before any action was taken."
    )
    assert not LOG_PATH.exists(), (
        f"Log file {LOG_PATH} already exists before any action was taken."
    )