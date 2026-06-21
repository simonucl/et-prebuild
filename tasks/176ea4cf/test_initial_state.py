# test_initial_state.py
#
# This pytest suite verifies the *initial* condition of the operating-system
# and filesystem before the student starts working on the assignment.
#
# It checks that:
#   • /home/user/logs exists and has the expected permissions.
#   • /home/user/logs/access.log exists, is readable, and looks like an
#     Apache access log (very loose regex ‑ we only want to be sure it is
#     a log file with IPv4 addresses in the first column).
#   • No analysis artefacts (/home/user/analysis, summary.log,
#     commands.log) exist yet.
#
# The tests purposefully do *not* check for any output of the student’s
# work — they only confirm the starting point is correct.
#
# Only the Python standard library and pytest are used.

import os
import re
import stat
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
ACCESS_LOG = LOG_DIR / "access.log"
ANALYSIS_DIR = Path("/home/user/analysis")
SUMMARY_LOG = ANALYSIS_DIR / "summary.log"
COMMANDS_LOG = ANALYSIS_DIR / "commands.log"

IPV4_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}\s")


def _human_perms(mode: int) -> str:
    """Return a human-readable representation of permission bits."""
    return oct(mode & 0o777)


def test_logs_directory_exists_with_correct_permissions():
    assert LOG_DIR.exists(), (
        "The directory /home/user/logs is missing. "
        "It must be present before the analysis begins."
    )
    assert LOG_DIR.is_dir(), "/home/user/logs exists but is not a directory."

    mode = LOG_DIR.stat().st_mode
    expected = 0o755
    assert (mode & 0o777) == expected, (
        f"/home/user/logs should have permissions 755 "
        f"(rwxr-xr-x) but has {_human_perms(mode)}."
    )


def test_access_log_exists_and_is_readable():
    assert ACCESS_LOG.exists(), (
        "The file /home/user/logs/access.log is missing. "
        "It must be provided for the investigation."
    )
    assert ACCESS_LOG.is_file(), "/home/user/logs/access.log exists but is not a regular file."

    mode = ACCESS_LOG.stat().st_mode
    expected = 0o644
    assert (mode & 0o777) == expected, (
        f"/home/user/logs/access.log should have permissions 644 "
        f"(rw-r--r--) but has {_human_perms(mode)}."
    )

    # Ensure the log is not empty and looks like an Apache access log.
    with ACCESS_LOG.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert lines, "/home/user/logs/access.log is empty — it should contain log lines to analyse."

    # Check the first few lines match a very loose Apache combined-log pattern:
    #   <IPv4> ... [timestamp] "METHOD /path HTTP/1.1" status bytes ...
    sample = lines[: min(5, len(lines))]
    for idx, line in enumerate(sample, start=1):
        assert IPV4_RE.match(line), (
            f"Line {idx} of access.log does not start with an IPv4 address. "
            "The file should be in standard Apache access-log format."
        )


def test_analysis_directory_does_not_exist_yet():
    assert not ANALYSIS_DIR.exists(), (
        "/home/user/analysis should not exist before the student runs their solution."
    )
    assert not SUMMARY_LOG.exists(), (
        "/home/user/analysis/summary.log should not exist before the student creates it."
    )
    assert not COMMANDS_LOG.exists(), (
        "/home/user/analysis/commands.log should not exist before the student creates it."
    )