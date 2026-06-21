# test_initial_state.py
#
# This pytest suite validates the initial filesystem state **before**
# the student performs any action.  It checks that:
#
# 1. /home/user/build exists and has the correct permissions.
# 2. /home/user/build/raw_artifacts.log exists, has the right
#    permissions, and its byte–for–byte contents match the truth.
# 3. /home/user/build/artifact_frequency.log is NOT present yet
#    (it will be produced by the student later).
#
# The assertions are written to give very clear error messages if
# anything is missing or out of place.
#
# Only the Python stdlib and pytest are used.

import os
import stat
import pwd
import grp
from pathlib import Path

BUILD_DIR = Path("/home/user/build")
RAW_LOG  = BUILD_DIR / "raw_artifacts.log"
OUTPUT_LOG = BUILD_DIR / "artifact_frequency.log"

EXPECTED_BUILD_MODE = 0o755  # drwxr-xr-x
EXPECTED_LOG_MODE   = 0o644  # -rw-r--r--

EXPECTED_RAW_CONTENT = (
    b"libfoo.so\n"
    b"libbar.so\n"
    b"libfoo.so\n"
    b"libbaz.so\n"
    b"libfoo.so\n"
    b"libbar.so\n"
    b"libqux.so\n"
)

def _mode(path: Path) -> int:
    """Return the permission bits of *path* (e.g. 0o755)."""
    return stat.S_IMODE(path.stat().st_mode)

def test_build_directory_exists_with_correct_permissions():
    assert BUILD_DIR.exists(), f"Required directory {BUILD_DIR} is missing."
    assert BUILD_DIR.is_dir(), f"{BUILD_DIR} exists but is not a directory."
    actual_mode = _mode(BUILD_DIR)
    assert actual_mode == EXPECTED_BUILD_MODE, (
        f"{BUILD_DIR} permissions are {oct(actual_mode)}, expected "
        f"{oct(EXPECTED_BUILD_MODE)}."
    )

def test_raw_artifacts_log_exists_with_correct_permissions_and_content():
    assert RAW_LOG.exists(), f"Required file {RAW_LOG} is missing."
    assert RAW_LOG.is_file(), f"{RAW_LOG} exists but is not a regular file."
    actual_mode = _mode(RAW_LOG)
    assert actual_mode == EXPECTED_LOG_MODE, (
        f"{RAW_LOG} permissions are {oct(actual_mode)}, expected "
        f"{oct(EXPECTED_LOG_MODE)}."
    )

    # Verify ownership (best-effort: only checked if 'user' account exists)
    try:
        expected_uid = pwd.getpwnam("user").pw_uid
        expected_gid = grp.getgrnam("user").gr_gid
        st = RAW_LOG.stat()
        assert st.st_uid == expected_uid, (
            f"{RAW_LOG} is owned by uid {st.st_uid}, expected uid {expected_uid} ('user')."
        )
        assert st.st_gid == expected_gid, (
            f"{RAW_LOG} is owned by gid {st.st_gid}, expected gid {expected_gid} ('user')."
        )
    except KeyError:
        # The executing environment might not have a 'user' account;
        # in that case, skip the ownership check gracefully.
        pass

    # Validate exact byte content.
    with RAW_LOG.open("rb") as fh:
        data = fh.read()
    assert data == EXPECTED_RAW_CONTENT, (
        f"{RAW_LOG} contents do not match expected data.\n\n"
        f"Expected ({len(EXPECTED_RAW_CONTENT)} bytes):\n"
        f"{EXPECTED_RAW_CONTENT!r}\n\n"
        f"Found ({len(data)} bytes):\n"
        f"{data!r}"
    )

def test_output_file_not_present_yet():
    assert not OUTPUT_LOG.exists(), (
        f"The output file {OUTPUT_LOG} should NOT exist before the student runs "
        "their solution."
    )