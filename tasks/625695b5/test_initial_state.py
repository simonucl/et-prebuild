# test_initial_state.py
#
# Pytest suite that validates the starting filesystem state **before**
# the student runs any rsync commands.  These checks guarantee that the
# predefined layout is in place and that no output artefacts are present
# yet.

import os
from pathlib import Path

HOME = Path("/home/user")

SOURCE_DIR = HOME / "source_project"
BACKUP_DIR = HOME / "backup_server"
RSYNC_LOG_DIR = HOME / "rsync_logs"


def _recursive_contents(path: Path):
    """
    Helper that yields every file and directory (including the given path)
    beneath *path*.  Returns pathlib.Path objects relative to *path* for
    simpler comparison.
    """
    for p in path.rglob("*"):
        yield p.relative_to(path)


def test_source_project_structure():
    """
    /home/user/source_project must exist and contain exactly:
        - index.html          (regular file)
        - script.js           (regular file)
        - assets/             (directory)
        - assets/style.css    (regular file)
    Nothing else may be present.
    """
    assert SOURCE_DIR.is_dir(), (
        f"Expected directory {SOURCE_DIR} is missing."
    )

    required_items = {
        Path("index.html"),
        Path("script.js"),
        Path("assets"),
        Path("assets/style.css"),
    }

    # Gather actual relative paths
    actual_items = set(_recursive_contents(SOURCE_DIR))

    # Check for missing items
    missing = required_items - actual_items
    assert not missing, (
        "The following required items are missing from "
        f"{SOURCE_DIR}: {', '.join(map(str, sorted(missing)))}"
    )

    # Check for unexpected extra items
    extras = actual_items - required_items
    assert not extras, (
        f"Unexpected files/directories found in {SOURCE_DIR}: "
        f"{', '.join(map(str, sorted(extras)))}"
    )

    # Type checks
    assert (SOURCE_DIR / "index.html").is_file(), "index.html must be a file."
    assert (SOURCE_DIR / "script.js").is_file(), "script.js must be a file."
    assert (SOURCE_DIR / "assets").is_dir(), "assets must be a directory."
    assert (
        SOURCE_DIR / "assets" / "style.css"
    ).is_file(), "assets/style.css must be a file."


def test_backup_server_is_empty_dir():
    """
    /home/user/backup_server must exist and be completely empty before the task
    begins.  This confirms that the student will populate it themselves.
    """
    assert BACKUP_DIR.is_dir(), (
        f"Expected directory {BACKUP_DIR} is missing."
    )

    # Any entry (file or directory) inside means it's not empty.
    contents = list(BACKUP_DIR.iterdir())
    assert not contents, (
        f"{BACKUP_DIR} is expected to be empty, but contains: "
        f"{', '.join(p.name for p in contents)}"
    )


def test_rsync_logs_dir_exists_and_writable():
    """
    /home/user/rsync_logs must exist and be writable by the current user so
    the student can create initial_sync.log there later.
    """
    assert RSYNC_LOG_DIR.is_dir(), (
        f"Expected directory {RSYNC_LOG_DIR} is missing."
    )

    # Check write permission using os.access for the real UID.
    can_write = os.access(RSYNC_LOG_DIR, os.W_OK)
    assert can_write, (
        f"The directory {RSYNC_LOG_DIR} is not writable by the current user."
    )