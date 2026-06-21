# test_initial_state.py
#
# Pytest suite that validates the pristine filesystem *before* the student
# begins the assignment.  It checks that the backup directory and its
# contents are exactly as described in the task specification.
#
# The tests **must** pass unchanged for the grader to continue; any failure
# means the initial state is wrong or has been tampered with.

import os
import stat
import pytest

HOME = "/home/user"
BACKUPS_DIR = f"{HOME}/backups"
SCRIPTS_DIR = f"{HOME}/backup_scripts"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _octal_mode(path):
    """Return the file mode as a zero-padded 3-digit octal string, e.g. '644'."""
    st_mode = os.stat(path, follow_symlinks=False).st_mode
    return f"{stat.S_IMODE(st_mode):03o}"

def _file_size(path):
    """Return file size in bytes."""
    return os.stat(path, follow_symlinks=False).st_size

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist_and_are_directories():
    """Verify that key directories exist and are directories."""
    for d in (BACKUPS_DIR, SCRIPTS_DIR):
        assert os.path.exists(d), f"Expected directory {d!r} to exist."
        assert os.path.isdir(d), f"Expected {d!r} to be a directory, got something else."


@pytest.mark.parametrize(
    "filename,expected_mode,expected_size",
    [
        ("prod_2023-09-01.sql", "600", 12345),
        ("prod_2023-09-02.sql", "660", 23456),
        ("prod_2023-09-03.sql", "666", 34567),
        ("staging_2023-09-01.dump", "644", 45678),
        ("staging_2023-09-02.dump", "606", 56789),
    ],
)
def test_backup_files_exist_with_correct_mode_and_size(filename, expected_mode, expected_size):
    """Each listed backup file must exist with the exact mode and size given."""
    path = os.path.join(BACKUPS_DIR, filename)
    assert os.path.exists(path), f"Expected file {path!r} to exist."
    assert os.path.isfile(path), f"{path!r} is expected to be a regular file."

    actual_mode = _octal_mode(path)
    assert actual_mode == expected_mode, (
        f"Incorrect permissions on {path!r}: expected {expected_mode}, found {actual_mode}"
    )

    actual_size = _file_size(path)
    assert actual_size == expected_size, (
        f"Incorrect size for {path!r}: expected {expected_size} bytes, found {actual_size} bytes"
    )


def test_no_extra_regular_files_in_backups_dir():
    """
    Ensure that no unexpected *regular* files (excluding dot-files) are present
    directly inside /home/user/backups/.
    """
    expected = {
        "prod_2023-09-01.sql",
        "prod_2023-09-02.sql",
        "prod_2023-09-03.sql",
        "staging_2023-09-01.dump",
        "staging_2023-09-02.dump",
    }

    actual = {
        entry.name
        for entry in os.scandir(BACKUPS_DIR)
        if entry.is_file(follow_symlinks=False) and not entry.name.startswith(".")
    }

    # Helpful diff in failure message
    extra = actual - expected
    missing = expected - actual
    assert not extra and not missing, (
        "Unexpected file set in /home/user/backups/.\n"
        f"Missing files: {sorted(missing)}\n"
        f"Extra files: {sorted(extra)}"
    )