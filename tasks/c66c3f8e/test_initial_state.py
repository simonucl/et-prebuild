# test_initial_state.py
#
# This test-suite validates the operating-system / filesystem *before*
# the student performs any action.  It asserts that the initial state
# described in the assignment is present and nothing has been modified
# yet.  All paths are checked with full absolute names.
#
# Only Python’s stdlib and pytest are used.

import os
import stat
import pwd
import grp
import pytest

HOME = "/home/user"
LOG_DIR = f"{HOME}/logs"
SYSTEM_LOG = f"{LOG_DIR}/system.log"
ANALYZED_DIR = f"{LOG_DIR}/analyzed"
SUMMARY_FILE = f"{ANALYZED_DIR}/summary-20230701.log"
PERM_REPORT = f"{ANALYZED_DIR}/perm_report.txt"

EXPECTED_SYSTEM_LOG_LINES = [
    "2023-07-01 12:00:01 FAILED LOGIN user=root",
    "2023-07-01 12:01:15 ERROR Disk quota exceeded",
    "2023-07-01 12:02:45 WARNING High memory usage detected",
    "2023-07-01 12:03:00 FAILED LOGIN user=admin",
    "2023-07-01 12:03:30 ERROR Cannot open configuration file",
    "2023-07-01 12:04:05 WARNING CPU temperature high",
    "2023-07-01 12:05:20 ERROR Invalid user input",
    "2023-07-01 12:06:10 FAILED LOGIN user=test",
    "2023-07-01 12:07:55 ERROR Service unavailable",
    "2023-07-01 12:08:30 ERROR Timeout while connecting to DB",
]

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------

def octal_mode(path: str) -> int:
    """Return the mode bits (e.g., 0o755) for a filesystem object."""
    return stat.S_IMODE(os.stat(path, follow_symlinks=False).st_mode)


def owner_group(path: str):
    """Return (owner_name, group_name) for a path."""
    st = os.stat(path, follow_symlinks=False)
    return pwd.getpwuid(st.st_uid).pw_name, grp.getgrgid(st.st_gid).gr_name


def current_user_group():
    """Return (login_user, current_primary_group)."""
    uid = os.getuid()
    gid = os.getgid()
    return pwd.getpwuid(uid).pw_name, grp.getgrgid(gid).gr_name


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_logs_directory_exists_and_perms():
    assert os.path.isdir(LOG_DIR), (
        f"Expected directory {LOG_DIR} to exist, but it is missing."
    )

    mode = octal_mode(LOG_DIR)
    assert mode == 0o755, (
        f"Directory {LOG_DIR} should have mode 755 (drwxr-xr-x), "
        f"but is {mode:03o}."
    )

    exp_user, exp_group = current_user_group()
    user, group = owner_group(LOG_DIR)
    assert user == exp_user, (
        f"Directory {LOG_DIR} should be owned by user '{exp_user}', "
        f"but owner is '{user}'."
    )
    assert group == exp_group, (
        f"Directory {LOG_DIR} should belong to group '{exp_group}', "
        f"but group is '{group}'."
    )


def test_system_log_exists_and_permissions():
    assert os.path.isfile(SYSTEM_LOG), (
        f"Expected file {SYSTEM_LOG} to exist, but it is missing."
    )

    mode = octal_mode(SYSTEM_LOG)
    assert mode == 0o644, (
        f"File {SYSTEM_LOG} should have mode 644 (-rw-r--r--), "
        f"but is {mode:03o}."
    )

    exp_user, exp_group = current_user_group()
    user, group = owner_group(SYSTEM_LOG)
    assert user == exp_user, (
        f"File {SYSTEM_LOG} should be owned by user '{exp_user}', "
        f"but owner is '{user}'."
    )
    assert group == exp_group, (
        f"File {SYSTEM_LOG} should belong to group '{exp_group}', "
        f"but group is '{group}'."
    )


def test_system_log_content_exact():
    with open(SYSTEM_LOG, "r", newline="") as fp:
        raw = fp.read()

    # Ensure UNIX LF endings only
    assert "\r" not in raw, f"{SYSTEM_LOG} contains CR characters (expected LF only)."

    lines = raw.splitlines()
    assert lines == EXPECTED_SYSTEM_LOG_LINES, (
        f"{SYSTEM_LOG} contents differ from specification.\n"
        f"Expected lines:\n{EXPECTED_SYSTEM_LOG_LINES}\n\n"
        f"Actual lines:\n{lines}"
    )

    # Additional sanity: token counts
    joined = "\n".join(lines)
    assert joined.count("FAILED LOGIN") == 3, "FAILED LOGIN count should be 3."
    assert joined.count("ERROR") == 5, "ERROR count should be 5."
    assert joined.count("WARNING") == 2, "WARNING count should be 2."


def test_analyzed_directory_not_present_yet():
    assert not os.path.exists(ANALYZED_DIR), (
        f"Directory {ANALYZED_DIR} should NOT exist before the student runs "
        "their solution."
    )


@pytest.mark.parametrize("p", [SUMMARY_FILE, PERM_REPORT])
def test_report_files_not_present_yet(p):
    assert not os.path.exists(p), (
        f"File {p} should NOT exist before the student generates reports."
    )