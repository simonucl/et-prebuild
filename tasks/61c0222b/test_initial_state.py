# test_initial_state.py
#
# Pytest suite that verifies the **initial** operating-system / filesystem
# state for the “one-off benchmark” task.
#
# A correct implementation MUST leave the system in the following state:
#   1. Directory  /home/user/benchmarks              exists.
#   2. File       /home/user/benchmarks/performance.log
#        • exists and is a regular text file
#        • permissions are no more permissive than 0644
#        • contains exactly three newline-terminated, non-blank lines
#          matching strict regexes defined below, in the stated order.
#
# These checks deliberately run *before* any student code is executed,
# guaranteeing that automated grading starts from a known good baseline.
#
# Only Python stdlib + pytest are used.

import os
import stat
import re
import pytest

BENCH_DIR = "/home/user/benchmarks"
LOG_FILE  = os.path.join(BENCH_DIR, "performance.log")


def test_benchmarks_directory_exists():
    """
    The directory /home/user/benchmarks must already exist
    and be a real directory (not a symlink, file, etc.).
    """
    assert os.path.isdir(BENCH_DIR), (
        f"Required directory missing: {BENCH_DIR!r}. "
        "Create it before running the benchmark."
    )


def test_performance_log_exists_and_is_regular_file():
    """
    The log file must exist and be a plain, regular file.
    """
    assert os.path.isfile(LOG_FILE), (
        f"Required log file missing or not a regular file: {LOG_FILE!r}. "
        "Did you create /home/user/benchmarks/performance.log?"
    )


def test_performance_log_permissions():
    """
    File permissions must be world-readable but NOT world-writable
    (i.e., numeric mode <= 0644).
    """
    mode = stat.S_IMODE(os.stat(LOG_FILE).st_mode)
    assert mode <= 0o644, (
        f"Incorrect permissions on {LOG_FILE}: {oct(mode)}. "
        "Permissions must be no more permissive than 0644."
    )


def test_performance_log_contents():
    """
    Validate exact content requirements:
      • exactly 3 lines
      • each line ends with '\n'
      • lines match regexes in required order
    """
    # Read the file as bytes so we can unambiguously check newlines
    with open(LOG_FILE, "rb") as fh:
        data = fh.read()

    assert data, "performance.log is empty."
    assert data.endswith(b"\n"), (
        "The final line of performance.log must be terminated by a newline (\\n)."
    )

    lines = data.splitlines()  # removes trailing '\n' chars
    assert len(lines) == 3, (
        f"performance.log must contain exactly 3 non-blank lines; "
        f"found {len(lines)}."
    )

    regexes = [
        re.compile(rb"^DISK_WRITE_MB_S: [0-9]+(\.[0-9]+)?$"),
        re.compile(rb"^CPU_EVENTS_PER_SEC: [0-9]+(\.[0-9]+)?$"),
        re.compile(rb"^TIMESTAMP: [0-9]{4}-[0-9]{2}-[0-9]{2} "
                   rb"[0-9]{2}:[0-9]{2}:[0-9]{2}$"),
    ]

    for idx, (line, pattern) in enumerate(zip(lines, regexes), start=1):
        assert pattern.match(line), (
            f"Line {idx} of performance.log does not match the required format.\n"
            f"  Expected regex: {pattern.pattern.decode()}\n"
            f"  Actual line   : {line.decode(errors='replace')}"
        )