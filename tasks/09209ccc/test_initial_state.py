# test_initial_state.py
#
# Pytest test-suite that validates the *initial* workstation state
# before the student creates the backup bundle.  It checks that
# 1) the source data hierarchy exists exactly as expected, and
# 2) the target backup directory (and the three deliverables that
#    will eventually go inside it) do **not** exist yet.
#
# Any failure message is written so that the student immediately
# knows what is missing or unexpectedly present.

import os
from pathlib import Path

# --- Constants ----------------------------------------------------------------

HOME = Path("/home/user")
SRC = HOME / "data_to_backup"
DST = HOME / "backups"

DOC1 = SRC / "doc1.txt"
PHOTO = SRC / "images" / "photo.jpg"
SCRIPT = SRC / "scripts" / "backup.sh"

ARCHIVE_FILE = DST / "data_backup.tar.gz"
MANIFEST_FILE = DST / "data_backup_manifest.log"
CHECKSUM_FILE = DST / "data_backup_checksums.log"


# --- Helper functions ---------------------------------------------------------

def _assert_exists(path: Path, is_dir: bool = False, *, explanation: str = ""):
    """Fail with a clear message if the given file/dir is absent or wrong type."""
    if not path.exists():
        raise AssertionError(f"Expected {path} to exist. {explanation}")
    if is_dir and not path.is_dir():
        raise AssertionError(f"Expected {path} to be a directory, "
                             f"but it is not. {explanation}")
    if not is_dir and not path.is_file():
        raise AssertionError(f"Expected {path} to be a regular file, "
                             f"but it is not. {explanation}")


def _assert_not_exists(path: Path, *, explanation: str = ""):
    """Fail if a file/dir exists when it should not."""
    if path.exists():
        raise AssertionError(f"{path} should NOT exist yet. {explanation}")


# --- Tests --------------------------------------------------------------------

def test_source_directory_structure_exists():
    """Validate that /home/user/data_to_backup exists and has the required tree."""
    _assert_exists(SRC, is_dir=True,
                   explanation="The data_to_backup directory must be provided by the task runner.")

    # Immediate sub-directories
    _assert_exists(SRC / "images", is_dir=True,
                   explanation="The 'images' directory is missing under data_to_backup.")
    _assert_exists(SRC / "scripts", is_dir=True,
                   explanation="The 'scripts' directory is missing under data_to_backup.")

    # Individual files
    _assert_exists(DOC1,
                   explanation="The source file 'doc1.txt' is missing.")
    _assert_exists(PHOTO,
                   explanation="The source file 'images/photo.jpg' is missing.")
    _assert_exists(SCRIPT,
                   explanation="The source file 'scripts/backup.sh' is missing.")


def test_source_file_contents():
    """Ensure text files contain exactly the expected bytes."""
    # doc1.txt must contain literal text "First document\n"
    expected_doc1 = "First document\n"
    with DOC1.open("r", encoding="utf-8") as fp:
        contents = fp.read()
    assert contents == expected_doc1, (
        f"{DOC1} contents are incorrect.\n"
        f"Expected: {repr(expected_doc1)}\n"
        f"Found   : {repr(contents)}"
    )

    # backup.sh must contain the simple two-line shell script
    expected_script = "#!/bin/bash\necho backup\n"
    with SCRIPT.open("r", encoding="utf-8") as fp:
        script_contents = fp.read()
    assert script_contents == expected_script, (
        f"{SCRIPT} contents are incorrect.\n"
        f"Expected: {repr(expected_script)}\n"
        f"Found   : {repr(script_contents)}"
    )


def test_photo_is_non_empty_binary():
    """The sample photo file must exist and be non-empty (exact bytes not checked)."""
    size = PHOTO.stat().st_size
    assert size > 0, f"{PHOTO} should be a non-empty binary file (found size={size})."


def test_backup_artifacts_do_not_exist_yet():
    """
    The student has not created any backup artifacts yet, so the entire
    /home/user/backups directory (and its expected contents) must be absent.
    """
    _assert_not_exists(ARCHIVE_FILE,
                       explanation="Archive file should be created only by the student's solution.")
    _assert_not_exists(MANIFEST_FILE,
                       explanation="Manifest file should be created only by the student's solution.")
    _assert_not_exists(CHECKSUM_FILE,
                       explanation="Checksum file should be created only by the student's solution.")

    # It is most helpful to check the directory *after* checking the individual
    # files, so the student sees the most specific message first.
    _assert_not_exists(DST,
                       explanation="The /home/user/backups directory should not exist before running the task.")