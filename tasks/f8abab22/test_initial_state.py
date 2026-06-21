# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student performs the required “move-and-log” action.
#
# DO NOT MODIFY THE TESTS.
# They describe the ground-truth layout that must exist *before*
# any solution command is executed.

from pathlib import Path
import re

BASE_DIR = Path("/home/user/db_backups")
ARCHIVE_DIR = BASE_DIR / "archive"
LOG_FILE = BASE_DIR / "backup_move.log"

# Expected filenames in their respective locations
PARENT_SQL_FILES = {
    "prod_full_2023-12-31.sql.gz",
    "prod_inc_2024-01-01.sql.gz",
    "prod_inc_2024-01-02.sql.gz",
}
ARCHIVE_SQL_FILE = "prod_full_2023-12-30.sql.gz"

# Expected (exact) contents of backup_move.log
EXPECTED_LOG_LINES = [
    "2024-02-15_10:00:00 moved 2 files",
    "2024-02-16_10:00:00 moved 1 files",
]


def test_directories_exist():
    assert BASE_DIR.is_dir(), (
        "Required directory /home/user/db_backups/ does not exist or is not a directory."
    )
    assert ARCHIVE_DIR.is_dir(), (
        "Required directory /home/user/db_backups/archive/ does not exist or is not a directory."
    )


def test_archive_contains_previous_backup():
    target = ARCHIVE_DIR / ARCHIVE_SQL_FILE
    assert target.is_file(), (
        f"Expected file {target} is missing from the archive directory."
    )


def test_parent_directory_contains_exact_sql_files():
    # Gather all *.sql.gz files in the parent directory
    existing = {p.name for p in BASE_DIR.glob("*.sql.gz")}
    missing = PARENT_SQL_FILES - existing
    extras = existing - PARENT_SQL_FILES

    assert not missing, (
        "The following required *.sql.gz files are missing from "
        f"/home/user/db_backups/: {', '.join(sorted(missing))}"
    )
    assert not extras, (
        "Unexpected *.sql.gz files found in /home/user/db_backups/: "
        f"{', '.join(sorted(extras))}"
    )


def test_readme_exists_with_correct_contents():
    readme = BASE_DIR / "readme.txt"
    assert readme.is_file(), "The file /home/user/db_backups/readme.txt is missing."

    expected_content = "Backups are dumped nightly.\n"
    actual = readme.read_text()
    assert actual == expected_content, (
        "readme.txt contents differ from expected.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Actual:   {repr(actual)}"
    )


def test_log_file_contents():
    assert LOG_FILE.is_file(), "The file /home/user/db_backups/backup_move.log is missing."

    lines = LOG_FILE.read_text().splitlines()
    assert lines == EXPECTED_LOG_LINES, (
        "backup_move.log must initially contain exactly two lines with the "
        "following contents:\n"
        + "\n".join(EXPECTED_LOG_LINES)
    )

    # Additionally verify the format with the grader's regex
    regex = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2} moved [0-9]+ files$")
    for i, line in enumerate(lines, start=1):
        assert regex.fullmatch(line), (
            f"Line {i} of backup_move.log does not match the required format:\n{line}"
        )