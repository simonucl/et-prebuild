# test_initial_state.py
#
# Pytest verification of the initial operating-system / filesystem
# state *before* the student performs any action for the
# “CPU-scheduling priority” exercise.
#
# Rules & assumptions are documented in the task description.
# This test suite checks only the prerequisites that must already
# hold when the student starts the task.

import os
import stat
import pytest

SCRIPT_PATH = "/home/user/db_long_query.sh"
EXPECTED_SCRIPT_CONTENT = (
    "#!/usr/bin/env bash\n"
    "# Simulates a CPU-intensive long query.\n"
    "while true; do :; done\n"
)


def _iter_proc_cmdlines():
    """
    Helper generator that yields (pid:int, cmdline:str) tuples for all
    accessible processes. The cmdline string preserves embedded NUL
    separators (`\\0`) exactly as read from /proc/<pid>/cmdline.
    """
    proc_root = "/proc"
    for entry in os.listdir(proc_root):
        if not entry.isdigit():
            continue
        pid = int(entry)
        cmdline_path = os.path.join(proc_root, entry, "cmdline")
        try:
            with open(cmdline_path, "rb") as fh:
                raw = fh.read()
            # Convert to a regular Python str while preserving embedded NULs
            cmdline = raw.decode(errors="replace")
        except (FileNotFoundError, PermissionError):
            # Skip kernel threads or permission-restricted entries
            continue
        yield pid, cmdline


def test_long_query_script_exists_and_is_executable():
    """Verify that the helper script exists with correct permissions and content."""
    assert os.path.isfile(
        SCRIPT_PATH
    ), f"Expected helper script at {SCRIPT_PATH}, but it does not exist."

    mode = os.stat(SCRIPT_PATH).st_mode
    is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"Helper script {SCRIPT_PATH} exists but is not executable "
        f"(mode {oct(mode & 0o777)}). Expected at least one execute bit."
    )

    with open(SCRIPT_PATH, "r", encoding="utf-8") as fh:
        content = fh.read()
    assert (
        content == EXPECTED_SCRIPT_CONTENT
    ), "Helper script content does not match the expected template."


def test_no_long_query_instances_running_initially():
    """
    Ensure that *no* instances of the helper script are running before
    the student starts their work.
    """
    matching_pids = []
    for pid, cmdline in _iter_proc_cmdlines():
        # A running instance will have the exact cmdline expected by the grader:
        #   bash\0/home/user/db_long_query.sh\0
        if cmdline.startswith("bash\0") and "/db_long_query.sh" in cmdline:
            matching_pids.append(pid)

    assert (
        not matching_pids
    ), (
        "Found running instances of db_long_query.sh before the task begins. "
        f"PIDs detected: {matching_pids}. The initial environment must be clean."
    )