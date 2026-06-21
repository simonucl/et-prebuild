# test_initial_state.py
#
# Pytest suite that validates the expected *initial* state of the
# filesystem before the student issues the required one–liner.
#
# What is verified
# ----------------
# 1. Presence of the four required directories.
# 2. Presence of /home/user/scripts/backup.sh, its executability, and
#    that it looks like the provided script (she-bang + tar invocation).
# 3. The optional log file, if present, contains only well-formed lines
#    (either the word SUCCESS or FAILURE, no whitespace).
#
# IMPORTANT:  Nothing here creates, deletes, or modifies any files; the
#             suite is read-only so that it does not interfere with the
#             forthcoming student action.

import os
import stat
import re
import pytest
from pathlib import Path

HOME = Path("/home/user")

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _assert_executable(path: Path) -> None:
    """
    Assert that the given path exists, is a regular file and is executable
    by *someone* (user, group or other).
    """
    if not path.exists():
        pytest.fail(f"Required script missing: {path!s}")
    if not path.is_file():
        pytest.fail(f"Expected a file at {path!s}, but found something else.")
    mode = path.stat().st_mode
    if not (mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)):
        pytest.fail(f"File {path!s} is not marked executable (expected chmod 755).")

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_required_directories_exist():
    """
    The four directories needed for the task must already exist.
    """
    required_dirs = [
        HOME / "scripts",
        HOME / "data" / "source_data",
        HOME / "backups",
        HOME / "logs",
    ]
    for d in required_dirs:
        assert d.is_dir(), (
            f"Required directory missing or not a directory: {d}"
        )


def test_backup_script_properties():
    """
    The backup script must be present, executable, and contain the expected
    she-bang and tar invocation.
    """
    script = HOME / "scripts" / "backup.sh"

    _assert_executable(script)

    # Basic content sanity check (read small header only, not entire file)
    try:
        with script.open("r", encoding="utf-8") as fh:
            lines = [fh.readline().rstrip("\n") for _ in range(5)]
    except Exception as exc:
        pytest.fail(f"Could not read {script}: {exc}")

    # She-bang on first line.
    assert lines and lines[0].startswith("#!"), (
        f"{script} does not start with a she-bang (#!) line."
    )

    # Must mention tar and the intended destination.
    snippet_ok = any("tar" in ln and "/home/user/backups" in ln for ln in lines)
    assert snippet_ok, (
        f"{script} does not appear to contain the expected tar invocation "
        "that writes into /home/user/backups."
    )


def test_optional_log_file_format():
    """
    The log file is optional at start-up.  If it *is* present, each existing
    line must already follow the 'SUCCESS' / 'FAILURE' convention so that
    the student does not inherit a malformed log.
    """
    log_path = HOME / "logs" / "backup_status.log"
    if not log_path.exists():
        pytest.skip("Log file does not yet exist; that is acceptable for the initial state.")

    # Empty file is fine.
    if log_path.stat().st_size == 0:
        return

    bad_lines = []
    valid_pattern = re.compile(r"^(SUCCESS|FAILURE)$")
    with log_path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            stripped = line.rstrip("\n")
            if not valid_pattern.fullmatch(stripped):
                bad_lines.append((lineno, stripped))

    assert not bad_lines, (
        f"Found malformed lines in {log_path}: "
        + ", ".join(f"line {ln}: {txt!r}" for ln, txt in bad_lines)
    )