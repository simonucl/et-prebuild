# test_initial_state.py
#
# This test-suite verifies that the **initial** filesystem state is exactly
# what the exercise specification promises – no more, no less.
#
# 1. /home/user/source_logs/        must already exist and contain *only*
#    the five specified files, each with the correct content.
# 2. No output artefacts created by the student’s solution may exist yet
#    (/home/user/backup_2023 directory or /home/user/backup_2023.tar.gz).
#
# Any deviation from these expectations will cause a descriptive failure,
# allowing students to recognise that their start-up environment is broken
# before they begin the actual task.
#
# NOTE:  Only stdlib + pytest are used, exactly as required.

from pathlib import Path
import pytest

SOURCE_DIR = Path("/home/user/source_logs")
BACKUP_DIR = Path("/home/user/backup_2023")
ARCHIVE    = Path("/home/user/backup_2023.tar.gz")

# --------------------------------------------------------------------------- #
# Expected initial files and their exact content (per specification)
# --------------------------------------------------------------------------- #
EXPECTED_CONTENT = {
    SOURCE_DIR / "app_server.log": [
        "2023-03-01 12:00:00 INFO Server started",
        "2023-03-01 12:05:00 ERROR Failed to connect to DB",
        "2023-03-01 12:10:00 INFO Retrying...",
        "2023-03-01 12:10:05 ERROR Retry failed",
        "2023-03-01 12:10:10 INFO Giving up",
        "2023-03-01 13:00:00 INFO Daily job executed",
        "2023-03-01 13:15:00 ERROR Daily job failed",
        "2023-03-01 13:16:00 INFO Notifying admin",
    ],
    SOURCE_DIR / "app_worker.log": [
        "2023-03-02 08:00:00 INFO Worker started",
        "2023-03-02 08:01:00 INFO Processing message 1",
        "2023-03-02 08:01:10 ERROR Message 1 failed",
        "2023-03-02 08:01:20 INFO Message 1 requeued",
        "2023-03-02 08:10:00 INFO Worker idle",
    ],
    SOURCE_DIR / "app_2022_old.log": [
        "2022-12-31 23:55:00 INFO Shutdown initiated",
        "2022-12-31 23:55:05 INFO Waiting for tasks",
        "2022-12-31 23:55:10 INFO Tasks complete",
        "2022-12-31 23:55:15 INFO Shutdown complete",
    ],
    SOURCE_DIR / "system.log": [
        "2023-03-03 09:00:00 INFO System check start",
        "2023-03-03 09:00:10 WARN CPU usage high",
        "2023-03-03 09:00:20 ERROR Fan failure",
        "2023-03-03 09:00:30 INFO Fan restart attempt",
        "2023-03-03 09:00:40 ERROR Fan restart failed",
        "2023-03-03 09:00:50 INFO Alarm triggered",
        "2023-03-03 09:01:00 INFO Cooling system engaged",
        "2023-03-03 09:01:10 INFO Logging event",
        "2023-03-03 09:01:20 INFO Event logged",
        "2023-03-03 09:01:30 INFO System check end",
    ],
    SOURCE_DIR / "readme.txt": [
        "These are demonstration logs used by the training task.",
    ],
}

EXPECTED_FILESET = set(EXPECTED_CONTENT.keys())

# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #
def _read_file_lines(path: Path):
    """
    Return the file content as a list of lines *without* the trailing newline
    characters so that we can compare cleanly against EXPECTED_CONTENT.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n\r") for ln in fh.readlines()]

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_source_directory_exists_and_is_dir():
    assert SOURCE_DIR.exists(), f"Required directory {SOURCE_DIR} is missing."
    assert SOURCE_DIR.is_dir(), f"{SOURCE_DIR} exists but is not a directory."

def test_source_directory_contains_expected_files_only():
    present_files = {p for p in SOURCE_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_FILESET - present_files
    unexpected = present_files - EXPECTED_FILESET
    assert not missing, (
        "The following required files are missing from "
        f"{SOURCE_DIR}:\n  " + "\n  ".join(str(p) for p in sorted(missing))
    )
    assert not unexpected, (
        "The following unexpected files are present in "
        f"{SOURCE_DIR} (should not be there yet):\n  "
        + "\n  ".join(str(p) for p in sorted(unexpected))
    )

@pytest.mark.parametrize("file_path,expected_lines", sorted(EXPECTED_CONTENT.items()))
def test_each_file_has_exact_expected_content(file_path: Path, expected_lines):
    assert file_path.exists(), f"Expected file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."
    actual_lines = _read_file_lines(file_path)
    assert (
        actual_lines == expected_lines
    ), (
        f"Content mismatch in {file_path}.\n"
        f"Expected ({len(expected_lines)} lines):\n  " +
        "\n  ".join(expected_lines[:10]) +  # show up to 10 lines for brevity
        ("\n  ... (truncated)" if len(expected_lines) > 10 else "") +
        "\n\nGot ({len(actual_lines)} lines):\n  " +
        "\n  ".join(actual_lines[:10]) +
        ("\n  ... (truncated)" if len(actual_lines) > 10 else "")
    )

def test_no_preexisting_backup_directory():
    assert (
        not BACKUP_DIR.exists()
    ), f"Directory {BACKUP_DIR} already exists – the workspace must start clean."

def test_no_preexisting_backup_archive():
    assert (
        not ARCHIVE.exists()
    ), f"Archive {ARCHIVE} already exists – it must be created by the student's solution, not beforehand."