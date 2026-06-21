# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# described in the assignment, i.e. *before* the student issues any
# commands.  The tests deliberately do **not** look for the later
# output file /home/user/artifact_manager/debug/missing_artifacts.log;
# that file is expected to be created by the student’s solution.

import os
from pathlib import Path

RELEASE_DIR = Path("/home/user/artifact_storage/releases")
INDEX_DIR = Path("/home/user/artifact_manager/index")
DEBUG_DIR = Path("/home/user/artifact_manager/debug")
INDEX_FILE = INDEX_DIR / "repository.index"

RELEASE_FILES = [
    "appserver-2.4.1.bin",
    "dbdriver-1.3.0.bin",
    "utils-0.9.8.bin",
]

# Exact, byte-for-byte contents expected inside repository.index
EXPECTED_INDEX_CONTENT = "appserver-2.4.1.bin\n" "dbdriver-1.3.0.bin\n"


def test_directories_exist_and_are_dirs():
    """Required top-level directories must exist and be directories."""
    for d in (RELEASE_DIR, INDEX_DIR, DEBUG_DIR):
        assert d.exists(), f"Expected directory {d} is missing."
        assert d.is_dir(), f"{d} exists but is not a directory."


def test_release_files_present_and_empty():
    """
    Every binary listed in the spec must be present in
    /artifact_storage/releases/ and must be an empty (0-byte) regular file.
    """
    for fname in RELEASE_FILES:
        fpath = RELEASE_DIR / fname
        assert fpath.exists(), f"Expected release file {fpath} is missing."
        assert fpath.is_file(), f"{fpath} exists but is not a regular file."
        size = fpath.stat().st_size
        assert size == 0, (
            f"{fpath} should be an empty placeholder file, "
            f"but it is {size} bytes."
        )


def test_repository_index_file_contents():
    """
    The repository.index file must exist and list ONLY the two binaries
    specified, each on its own line, with exactly one trailing newline.
    """
    assert INDEX_FILE.exists(), "repository.index file is missing."
    assert INDEX_FILE.is_file(), "repository.index exists but is not a file."

    contents = INDEX_FILE.read_text(encoding="utf-8")
    assert (
        contents == EXPECTED_INDEX_CONTENT
    ), (
        "repository.index contents do not match the expected pre-task state.\n"
        f"Expected:\n{EXPECTED_INDEX_CONTENT!r}\n"
        f"Found:\n{contents!r}"
    )


def test_output_file_not_yet_present():
    """
    The log file that the student must create should NOT exist yet.
    This guards against accidental pre-population.
    """
    log_path = DEBUG_DIR / "missing_artifacts.log"
    assert not log_path.exists(), (
        f"Output file {log_path} should not exist before the task is run."
    )