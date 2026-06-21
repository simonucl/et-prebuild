# test_initial_state.py
#
# Pytest suite that validates the machine’s initial state *before* the student
# starts working on the “mixed-encoding to UTF-8 conversion” task.
#
# Expectations for the pristine environment:
#   1. The three source files are present exactly where promised.
#   2. Each source file can be decoded with its documented legacy encoding.
#   3. No UTF-8 “.utf8.txt” copies exist yet.
#   4. The workspace /home/user/encoding_conversion/ (and the CSV log inside it)
#      do not exist yet.
#
# Only stdlib + pytest are used.

import os
import pathlib
import codecs
import pytest

HOME = pathlib.Path("/home/user")
DATA_DIR = HOME / "data"

# ---------------------------------------------------------------------------
# Reference information taken from the task description.
# ---------------------------------------------------------------------------

SOURCES = {
    "latin1_report.txt": "ISO-8859-1",
    "shiftjis_notes.txt": "Shift_JIS",
    "windows1252_legacy.txt": "Windows-1252",
}

TARGET_SUFFIX = ".utf8.txt"
WORKSPACE_DIR = HOME / "encoding_conversion"
LOG_FILE = WORKSPACE_DIR / "conversion_log.csv"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def get_source_path(filename: str) -> pathlib.Path:
    """Return the full Path object of a source file located in DATA_DIR."""
    return DATA_DIR / filename


def get_target_path(filename: str) -> pathlib.Path:
    """Return the would-be UTF-8 target path for a given source file."""
    basename = pathlib.Path(filename).stem             # "latin1_report"
    return DATA_DIR / f"{basename}{TARGET_SUFFIX}"     # …/latin1_report.utf8.txt


# ---------------------------------------------------------------------------
# Tests for the pristine filesystem state
# ---------------------------------------------------------------------------

def test_data_directory_exists():
    """The /home/user/data directory must exist and be a directory."""
    assert DATA_DIR.exists(), (
        f"Required directory {DATA_DIR} is missing. "
        "The automated grader expects the original data files there."
    )
    assert DATA_DIR.is_dir(), (
        f"{DATA_DIR} exists but is not a directory. "
        "Please ensure the testing image is set up correctly."
    )


@pytest.mark.parametrize("filename,encoding", SOURCES.items())
def test_source_files_exist_and_decodable(filename, encoding):
    """
    Each original file must exist *and* be decodable with the encoding
    advertised in the task description.  We do **not** validate content,
    merely that the bytes round-trip without error.
    """
    path = get_source_path(filename)
    assert path.exists(), (
        f"Source file {path} is missing. The student cannot begin without it."
    )
    assert path.is_file(), f"{path} exists but is not a regular file."

    # Attempt to decode the entire file with the expected encoding.
    # Any UnicodeDecodeError would signal a mismatch or corruption.
    try:
        with path.open("rb") as fh:
            raw_bytes = fh.read()
        # Using codecs.decode to be explicit about the operation
        _ = codecs.decode(raw_bytes, encoding)
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"File {path} could not be decoded with declared encoding "
            f"'{encoding}': {exc}"
        )


@pytest.mark.parametrize("filename", SOURCES.keys())
def test_no_utf8_target_files_yet(filename):
    """
    The UTF-8 working copies must *not* exist before the student runs
    their conversion script.
    """
    target_path = get_target_path(filename)
    assert not target_path.exists(), (
        f"Unexpected file {target_path} already exists. "
        "The environment must start without any .utf8.txt files."
    )


def test_workspace_and_log_absent():
    """
    The conversion workspace directory and the CSV log file must not exist
    in the pristine image.
    """
    assert not WORKSPACE_DIR.exists(), (
        f"Workspace directory {WORKSPACE_DIR} already exists. "
        "The student is supposed to create it during the task."
    )

    # Even if the directory does not exist, explicitly check the log file
    # in case something odd created only the file.
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} already exists. "
        "The student has to generate it as part of their deliverables."
    )