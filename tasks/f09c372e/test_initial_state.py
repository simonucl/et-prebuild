# test_initial_state.py
#
# This pytest suite confirms the *initial* operating-system state **before**
# the student launches any HTTP file server or writes a launch log.
#
# Truth source (summarised):
#   • /home/user/backups/         – exists (0755) with two specific files.
#   • /home/user/backup_server/   – exists (0755) and is empty.
#   • No file /home/user/backup_server/launch.log yet.
#   • Nothing is listening on TCP port 8080 at this moment.
#
# The tests purposely *do not* look for any result of the task itself; they
# merely assert that the starting point matches the specification so that any
# subsequent grading is meaningful.

import os
import stat
import socket
from pathlib import Path

BACKUPS_DIR = Path("/home/user/backups")
BACKUP_SERVER_DIR = Path("/home/user/backup_server")
LAUNCH_LOG = BACKUP_SERVER_DIR / "launch.log"

FILE_1 = BACKUPS_DIR / "full_2024_03_25.sql"
FILE_2 = BACKUPS_DIR / "incremental_2024_03_26.sql.gz"


def assert_mode_0755(path: Path) -> None:
    """
    Helper that asserts a path has exactly 0o755 permissions.
    Produces a clear pytest assertion message on failure.
    """
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode == 0o755, f"{path} exists but has permissions {oct(mode)}, expected 0o755"


def test_backups_directory_structure():
    """/home/user/backups must exist (0755) and contain the two expected files."""
    # Directory exists and is a real directory.
    assert BACKUPS_DIR.exists(), f"Expected directory {BACKUPS_DIR} to exist"
    assert BACKUPS_DIR.is_dir(), f"{BACKUPS_DIR} exists but is not a directory"

    # Permissions.
    assert_mode_0755(BACKUPS_DIR)

    # Expected files.
    for p in (FILE_1, FILE_2):
        assert p.exists(), f"Expected file {p} to be present in {BACKUPS_DIR}"
        assert p.is_file(), f"{p} exists but is not a regular file"


def test_backup_server_directory_empty():
    """
    /home/user/backup_server must exist (0755) and be empty before the task starts.
    """
    assert BACKUP_SERVER_DIR.exists(), f"Expected directory {BACKUP_SERVER_DIR} to exist"
    assert BACKUP_SERVER_DIR.is_dir(), f"{BACKUP_SERVER_DIR} exists but is not a directory"

    assert_mode_0755(BACKUP_SERVER_DIR)

    contents = list(BACKUP_SERVER_DIR.iterdir())
    assert not contents, (
        f"{BACKUP_SERVER_DIR} should be empty before the task starts, "
        f"but contains: {[p.name for p in contents]}"
    )


def test_launch_log_absent():
    """The launch log must not exist prior to running the student's command."""
    assert not LAUNCH_LOG.exists(), (
        f"{LAUNCH_LOG} should NOT exist yet; it must be created only after the server is launched."
    )


def _port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Returns True if a TCP connection to (host, port) succeeds within *timeout* seconds.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def test_nothing_listening_on_port_8080():
    """
    No process should be listening on TCP port 8080 yet.  The student’s
    eventual solution will start the server; this pre-check ensures the port
    is free so that later tests can attribute a listener to the student’s
    action rather than a pre-existing service.
    """
    assert not _port_open("127.0.0.1", 8080), (
        "Something is already listening on TCP port 8080 before the task starts. "
        "The port should be free at the beginning so the student can bind to it."
    )