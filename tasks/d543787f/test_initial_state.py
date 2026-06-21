# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem is in the
# expected “starting point” state *before* the student’s automation runs.
#
# Rules enforced:
#   1. /home/user/configs exists and is a directory.
#   2. It contains exactly two regular, non-hidden files: app.conf and db.conf.
#   3. The content of each file matches the specification.
#   4. /home/user/archives MUST NOT exist yet.
#   5. /home/user/config_change.log MUST NOT exist yet.
#
# Any failure message should make it clear what is missing or unexpected.
#
# Only stdlib + pytest is used.
import os
from pathlib import Path

CONFIGS_DIR = Path("/home/user/configs")
ARCHIVES_DIR = Path("/home/user/archives")
LOG_FILE = Path("/home/user/config_change.log")

EXPECTED_FILES = {
    "app.conf": "APP_NAME=TestApp\nAPP_ENV=production\n",
    "db.conf": "DB_HOST=localhost\nDB_PORT=5432\n",
}


def test_configs_dir_exists_and_is_dir():
    assert CONFIGS_DIR.exists(), (
        f"Expected directory {CONFIGS_DIR} to exist but it does not."
    )
    assert CONFIGS_DIR.is_dir(), (
        f"Expected {CONFIGS_DIR} to be a directory but it is not."
    )


def test_configs_contains_expected_files_only():
    """
    The directory must contain exactly the two specified configuration files
    and nothing else (no extra regular, non-hidden files).
    """
    entries = [
        p.name
        for p in CONFIGS_DIR.iterdir()
        if p.is_file() and not p.name.startswith(".")
    ]
    assert sorted(entries) == sorted(EXPECTED_FILES.keys()), (
        f"{CONFIGS_DIR} should contain exactly the files "
        f"{sorted(EXPECTED_FILES.keys())}, but it contains {sorted(entries)}."
    )


def _read_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


def test_configs_file_contents():
    for filename, expected_content in EXPECTED_FILES.items():
        file_path = CONFIGS_DIR / filename
        assert file_path.exists(), (
            f"Expected file {file_path} to exist but it does not."
        )
        assert file_path.is_file(), (
            f"Expected {file_path} to be a regular file."
        )
        actual_content = _read_file(file_path)
        assert actual_content == expected_content, (
            f"Content mismatch for {file_path}.\n"
            f"Expected:\n{expected_content!r}\n"
            f"Actual:\n{actual_content!r}"
        )


def test_archives_dir_absent():
    assert not ARCHIVES_DIR.exists(), (
        f"The directory {ARCHIVES_DIR} should NOT exist before the automation "
        f"runs, but it does."
    )


def test_log_file_absent():
    assert not LOG_FILE.exists(), (
        f"The file {LOG_FILE} should NOT exist before the automation runs, "
        f"but it does."
    )