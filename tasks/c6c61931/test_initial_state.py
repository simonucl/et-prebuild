# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the learner fixes the broken “latest.log” symlink.
#
# Assumptions about the pristine environment:
#   /home/user/logs/
#       app-2023-12-30.log      (regular file)
#       app-2023-12-31.log      (regular file)
#       latest.log  -> app-2023-12-30.log   (symlink)
#
# Nothing else should be present that is relevant to the upcoming task,
# especially *link_verification.txt* which must **not** exist yet.
#
# The tests below purposely fail fast and with clear messages if the
# sandbox is not in the expected initial state.

import os
import stat
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
LOG_30 = LOG_DIR / "app-2023-12-30.log"
LOG_31 = LOG_DIR / "app-2023-12-31.log"
LATEST = LOG_DIR / "latest.log"
VERIFICATION = LOG_DIR / "link_verification.txt"


def _is_regular_file(path: Path) -> bool:
    """Return True iff path exists and is a *regular* file (not symlink)."""
    try:
        st = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISREG(st.st_mode)


def _is_symlink(path: Path) -> bool:
    """Return True iff path exists and is a symbolic link."""
    return path.exists() and path.is_symlink()


def test_log_directory_exists():
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} to exist."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_expected_log_files_present_and_regular():
    for logfile in (LOG_30, LOG_31):
        assert _is_regular_file(logfile), (
            f"Expected regular file {logfile} to exist (not a symlink)."
        )


def test_latest_log_is_symlink_to_previous_day():
    assert _is_symlink(LATEST), f"Expected {LATEST} to be a symbolic link."
    target = os.readlink(LATEST)
    assert (
        target == LOG_30.name
    ), (
        f"{LATEST} should point to {LOG_30.name} initially, "
        f"but it points to '{target}'."
    )


def test_verification_file_absent():
    assert not VERIFICATION.exists(), (
        f"{VERIFICATION} should NOT exist in the initial state."
    )