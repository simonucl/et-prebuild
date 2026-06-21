# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state that must be present *before* the student performs any actions.
#
# It intentionally makes **no assertions** about the “/home/user/monitoring”
# work-area that the student is expected to create; that directory is part of
# the *output* specification and is therefore outside the scope of these
# initial-state checks.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"

EXPECTED_LOG_FILES = {
    "web.log": "[web] Service started successfully.\n",
    "api.log": "[api] Service started successfully.\n",
    "db.log":  "[db] Service started successfully.\n",
}

@pytest.fixture(scope="module")
def logs_dir():
    """Return the Path object for /home/user/logs after validating its existence."""
    assert LOGS_DIR.exists(), f"Expected directory {LOGS_DIR} to exist."
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."
    return LOGS_DIR


def test_logs_directory_permissions_and_owner(logs_dir):
    """logs directory should be owned by the current user and mode 0755."""
    st = logs_dir.stat()
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o755, (
        f"{logs_dir} has mode {oct(mode)}, expected 0o755."
    )
    assert st.st_uid == os.getuid(), (
        f"{logs_dir} is owned by UID {st.st_uid}, "
        f"but expected current UID {os.getuid()}."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_LOG_FILES.items())
def test_log_file_exists_and_regular(logs_dir, filename, expected_content):
    """Each canonical log file must exist, be a regular file (not symlink), and readable."""
    fpath = logs_dir / filename
    assert fpath.exists(), f"Missing log file: {fpath}"
    assert fpath.is_file(), f"{fpath} exists but is not a regular file."
    # Ensure it's not a symlink
    assert not fpath.is_symlink(), f"{fpath} should be a regular file, not a symlink."

    # File permissions and ownership
    st = fpath.stat()
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o644, f"{fpath} has mode {oct(mode)}, expected 0o644."
    assert st.st_uid == os.getuid(), (
        f"{fpath} is owned by UID {st.st_uid}, expected current UID {os.getuid()}."
    )

    # File content
    content = fpath.read_text(encoding="utf-8")
    assert content == expected_content, (
        f"Unexpected content in {fpath}.\n"
        f"Expected exactly: {expected_content!r}\n"
        f"Actual content:   {content!r}"
    )

    # Ensure exactly one line
    num_lines = content.count("\n")
    assert num_lines == 1, (
        f"{fpath} should contain exactly one newline; found {num_lines} newlines."
    )


def test_no_extra_files_in_logs_directory(logs_dir):
    """/home/user/logs should contain *only* the expected log files, no extras."""
    present_files = {p.name for p in logs_dir.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_LOG_FILES)
    extras = present_files - expected_files
    missing = expected_files - present_files

    assert not missing, f"The following required log files are missing: {', '.join(sorted(missing))}"
    assert not extras, f"The following unexpected files are present in {logs_dir}: {', '.join(sorted(extras))}"