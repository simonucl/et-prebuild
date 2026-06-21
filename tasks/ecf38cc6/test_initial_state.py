# test_initial_state.py
#
# Pytest suite to validate the initial filesystem state **before** the student
# starts working on the “pipeline logs backup” task.
#
# This test file assumes the following initial truth:
#
# * /home/user/ci_artifacts/ exists and contains exactly three plaintext log
#   files: build.log, test.log, deploy.log with the exact line-by-line contents
#   described in the task statement.
# * /home/user/ci_cd_archives/ exists and is completely empty.
# * /home/user/task_output/ exists and is completely empty.
# * /home/user/ci_artifacts/extracted/ does NOT exist yet.
#
# Any deviation from this state should fail with a clear, descriptive message.

from pathlib import Path
import os
import pytest

HOME = Path("/home/user")

CI_ARTIFACTS_DIR = HOME / "ci_artifacts"
CI_CD_ARCHIVES_DIR = HOME / "ci_cd_archives"
TASK_OUTPUT_DIR = HOME / "task_output"
EXTRACTED_DIR = CI_ARTIFACTS_DIR / "extracted"
ARCHIVE_PATH = CI_CD_ARCHIVES_DIR / "pipeline_logs_backup.tar.gz"

EXPECTED_LOG_FILES = {
    "build.log": [
        "BUILD START",
        "Compiling modules...",
        "All modules compiled.",
        "BUILD END",
        "Status: SUCCESS",
    ],
    "test.log": [
        "TEST SUITE START",
        "All 128 tests passed.",
        "Duration: 00:01:34",
        "TEST SUITE END",
    ],
    "deploy.log": [
        "DEPLOYMENT START",
        "Pushing container to registry...",
        "Container SHA: abcdef123456",
        "Scaling services...",
        "DEPLOYMENT END",
        "Status: SUCCESS",
    ],
}


def _read_lines(path: Path):
    """Return the file's lines without trailing newline characters."""
    with path.open("rt", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


def test_ci_artifacts_directory_and_logs_exist_with_correct_content():
    # Directory presence
    assert CI_ARTIFACTS_DIR.is_dir(), (
        f"Expected directory {CI_ARTIFACTS_DIR} to exist."
    )

    # Collect actual files inside ci_artifacts
    actual_files = sorted(p.name for p in CI_ARTIFACTS_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_LOG_FILES.keys())
    assert actual_files == expected_files, (
        "The /home/user/ci_artifacts/ directory must contain *only* "
        f"{expected_files}, but found {actual_files}."
    )

    # Verify each log file exists and has the exact contents
    for filename, expected_lines in EXPECTED_LOG_FILES.items():
        file_path = CI_ARTIFACTS_DIR / filename
        assert file_path.is_file(), f"Missing expected log file: {file_path}"
        actual_lines = _read_lines(file_path)
        assert actual_lines == expected_lines, (
            f"Contents of {file_path} do not match expected content.\n"
            f"Expected lines:\n{expected_lines}\nActual lines:\n{actual_lines}"
        )


def test_ci_cd_archives_directory_exists_and_is_empty():
    assert CI_CD_ARCHIVES_DIR.is_dir(), (
        f"Expected directory {CI_CD_ARCHIVES_DIR} to exist."
    )

    contents = list(CI_CD_ARCHIVES_DIR.iterdir())
    assert not contents, (
        f"Directory {CI_CD_ARCHIVES_DIR} must be empty before the task starts, "
        f"but contains: {[p.name for p in contents]}"
    )


def test_task_output_directory_exists_and_is_empty():
    assert TASK_OUTPUT_DIR.is_dir(), (
        f"Expected directory {TASK_OUTPUT_DIR} to exist."
    )

    contents = list(TASK_OUTPUT_DIR.iterdir())
    assert not contents, (
        f"Directory {TASK_OUTPUT_DIR} must be empty before the task starts, "
        f"but contains: {[p.name for p in contents]}"
    )


def test_pipeline_backup_archive_and_extracted_dir_do_not_exist_yet():
    # The backup archive should not be present at the start.
    assert not ARCHIVE_PATH.exists(), (
        f"Archive {ARCHIVE_PATH} should NOT exist before the task starts."
    )

    # The extracted directory should also not be present at the start.
    assert not EXTRACTED_DIR.exists(), (
        f"Directory {EXTRACTED_DIR} should NOT exist before the task starts."
    )