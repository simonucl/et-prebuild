# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student performs any actions for the “API backup” task.
#
# The checker asserts that
#   • /home/user/api_samples/ exists and contains exactly three JSON files
#     whose byte-for-byte contents are known in advance.
#   • No artefacts that the student is supposed to create later
#     (archive, restore directory, log lines) are present yet.
#
# If any of these pre-conditions fail, something is wrong with the
# provisioning of the exercise environment, and the student should not start
# the task.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")

API_SAMPLES_DIR = HOME / "api_samples"
EXPECTED_FILES = {
    "sample1.json": '''{
  "id": 1,
  "status": "ok",
  "data": "alpha"
}
''',
    "sample2.json": '''{
  "id": 2,
  "status": "ok",
  "data": "beta"
}
''',
    "sample3.json": '''{
  "id": 3,
  "status": "ok",
  "data": "gamma"
}
''',
}

ARCHIVE_PATH = HOME / "api_backup.tar.gz"
RESTORE_DIR = HOME / "restore_test"
BACKUP_LOG = HOME / "backup.log"

# ---------------------------------------------------------------------------


def test_api_samples_directory_exists_and_is_directory():
    assert API_SAMPLES_DIR.exists(), (
        f"Required directory {API_SAMPLES_DIR} is missing. "
        "The exercise must start with this directory in place."
    )
    assert API_SAMPLES_DIR.is_dir(), (
        f"{API_SAMPLES_DIR} exists but is not a directory."
    )


def test_api_samples_directory_contains_exactly_expected_files():
    # Collect only regular files (no sub-directories, sockets, etc.)
    present = sorted(p.name for p in API_SAMPLES_DIR.iterdir() if p.is_file())
    expected = sorted(EXPECTED_FILES.keys())
    assert present == expected, (
        f"{API_SAMPLES_DIR} must contain exactly the files "
        f"{expected}, but the current contents are {present}."
    )


@pytest.mark.parametrize("filename, expected_content", EXPECTED_FILES.items())
def test_each_sample_file_content_matches_reference(filename, expected_content):
    file_path = API_SAMPLES_DIR / filename
    content = file_path.read_text(encoding="utf-8")
    assert content == expected_content, (
        f"File {file_path} is present but its contents do not match the "
        "expected reference data. The initial fixtures appear to be corrupt."
    )


def test_archive_does_not_yet_exist():
    assert not ARCHIVE_PATH.exists(), (
        f"{ARCHIVE_PATH} already exists, but it must not be present before "
        "the student creates it."
    )


def test_restore_test_directory_does_not_yet_exist():
    assert not RESTORE_DIR.exists(), (
        f"{RESTORE_DIR} already exists, but it must not be present before "
        "the student extracts the archive."
    )


def test_backup_log_not_yet_appended():
    """
    The backup.log file may or may not exist initially.  If it exists,
    it must *not* yet contain the two fixed log lines that the student
    is expected to append.
    """
    required_lines = [
        "2024-01-15T00:00:00 | ARCHIVE_CREATED   | /home/user/api_backup.tar.gz\n",
        "2024-01-15T00:00:05 | ARCHIVE_EXTRACTED | /home/user/restore_test/\n",
    ]

    if not BACKUP_LOG.exists():
        # Nothing to check further; it is acceptable that the file is absent.
        return

    text = BACKUP_LOG.read_text(encoding="utf-8")
    for line in required_lines:
        assert line not in text, (
            f"{BACKUP_LOG} already contains the line:\n{line!r}\n"
            "It must be appended only *after* the student completes the task."
        )