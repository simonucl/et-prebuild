# test_initial_state.py
#
# Pytest suite that verifies the machine’s *initial* state
# before the learner performs any tasks for the “network-debug
# backup” exercise.
#
# The expectations come straight from the task description:
#
# 1. /home/user/debug_logs/ **must exist** and contain exactly the
#    three files ping.log, traceroute.log, interface_status.log.
#
# 2. The three files must each be regular files, be UTF-8 text,
#    have the expected line counts (7 / 4 / 4), and use LF line
#    endings only.
#
# 3. The directories /home/user/archive/ and
#    /home/user/restored_logs/ must *not* exist yet, nor the
#    archive /home/user/archive/net_debug_backup.tar.gz, nor the
#    report /home/user/restored_logs/verification.txt.
#
# Any deviation from the prescribed state will make the test
# fail with a clear error message.
#
# NOTE:  Uses only stdlib + pytest.

from pathlib import Path
import io
import os
import pytest

HOME = Path("/home/user").resolve()
DEBUG_DIR = HOME / "debug_logs"
ARCHIVE_DIR = HOME / "archive"
RESTORED_DIR = HOME / "restored_logs"
ARCHIVE_FILE = ARCHIVE_DIR / "net_debug_backup.tar.gz"
VERIFICATION_FILE = RESTORED_DIR / "verification.txt"

EXPECTED_FILES = {
    "ping.log": 7,
    "traceroute.log": 4,
    "interface_status.log": 4,
}


def _read_lines(path: Path):
    """
    Read file as UTF-8 text and return a list of lines preserving
    line endings (so we can ensure LF only).
    """
    with path.open("rb") as fh:
        raw = fh.read()

    # Ensure no CR characters – blanket check for Windows endings.
    assert b"\r" not in raw, (
        f"{path} contains CR characters (\\r); "
        "only LF (\\n) line endings are expected."
    )

    # Decode as UTF-8; will raise if invalid.
    text = raw.decode("utf-8")
    return text.splitlines(keepends=True)


def test_debug_logs_directory_exists_and_is_correct():
    assert DEBUG_DIR.is_dir(), (
        f"Required directory {DEBUG_DIR} is missing."
    )

    # Collect actual files (ignore sub-directories just in case)
    actual_files = {p.name for p in DEBUG_DIR.iterdir() if p.is_file()}
    expected_set = set(EXPECTED_FILES.keys())

    assert actual_files == expected_set, (
        f"{DEBUG_DIR} should contain ONLY the three log files "
        f"{sorted(expected_set)}, but it contains {sorted(actual_files)} instead."
    )


@pytest.mark.parametrize("filename, expected_lines", EXPECTED_FILES.items())
def test_each_log_file_linecount_and_format(filename, expected_lines):
    path = DEBUG_DIR / filename
    assert path.is_file(), f"Expected file {path} is missing."

    lines = _read_lines(path)
    assert len(lines) == expected_lines, (
        f"{filename} should have {expected_lines} lines, "
        f"but has {len(lines)}."
    )

    # Ensure every line ends with LF.
    for idx, line in enumerate(lines, 1):
        assert line.endswith("\n"), (
            f"Line {idx} of {filename} is missing the required LF newline."
        )


def test_no_archive_directory_yet():
    assert not ARCHIVE_DIR.exists(), (
        f"{ARCHIVE_DIR} exists but should NOT be present before the task is started."
    )


def test_no_restored_directory_yet():
    assert not RESTORED_DIR.exists(), (
        f"{RESTORED_DIR} exists but should NOT be present before the task is started."
    )


def test_archive_and_verification_files_absent():
    assert not ARCHIVE_FILE.exists(), (
        f"Archive {ARCHIVE_FILE} already exists; the learner has not yet created it."
    )
    assert not VERIFICATION_FILE.exists(), (
        f"Verification file {VERIFICATION_FILE} already exists; "
        "it must be created only after extraction."
    )