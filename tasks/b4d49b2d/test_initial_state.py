# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem state before the student
# starts working on the “Grafana dashboard frequency” task.
#
# It checks only the pre-existing artefacts and explicitly avoids asserting
# anything about the artefacts that must be created by the student
# (e.g. /home/user/metrics/dashboard_frequency.txt).

import os
import pwd
import stat
import pytest

# Constants -------------------------------------------------------------------

METRICS_DIR = "/home/user/metrics"
HITS_LOG = os.path.join(METRICS_DIR, "dashboard_hits.log")

EXPECTED_LINES = [
    "dashboard_cpu",
    "dashboard_memory",
    "dashboard_cpu",
    "dashboard_cpu",
    "dashboard_network",
    "dashboard_memory",
    "dashboard_disk",
    "dashboard_network",
    "dashboard_network",
    "dashboard_disk",
]

EXPECTED_PERMS = 0o644  # rw-r--r-- (octal)


# Helper ----------------------------------------------------------------------


def _file_mode(path):
    """Return the permission bits (e.g. 0o644) of *path*."""
    return stat.S_IMODE(os.stat(path).st_mode)


# Tests -----------------------------------------------------------------------


def test_metrics_directory_exists_and_is_dir():
    assert os.path.exists(METRICS_DIR), (
        f"Required directory {METRICS_DIR!r} does not exist."
    )
    assert os.path.isdir(METRICS_DIR), (
        f"{METRICS_DIR!r} exists but is not a directory."
    )


def test_hits_log_exists_and_is_file():
    assert os.path.exists(HITS_LOG), (
        f"Required log file {HITS_LOG!r} is missing."
    )
    assert os.path.isfile(HITS_LOG), (
        f"{HITS_LOG!r} exists but is not a regular file."
    )


def test_hits_log_permissions():
    mode = _file_mode(HITS_LOG)
    assert mode == EXPECTED_PERMS, (
        f"{HITS_LOG!r} permissions expected to be "
        f"{oct(EXPECTED_PERMS)}, found {oct(mode)}."
    )


def test_hits_log_ownership_matches_current_user():
    st = os.stat(HITS_LOG)
    current_uid = os.getuid()
    current_user = pwd.getpwuid(current_uid).pw_name
    file_user = pwd.getpwuid(st.st_uid).pw_name
    assert st.st_uid == current_uid, (
        f"{HITS_LOG!r} should be owned by the current user "
        f"({current_user}), but is owned by {file_user}."
    )


def test_hits_log_contents_match_expected():
    with open(HITS_LOG, "rt", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines()]

    assert lines == EXPECTED_LINES, (
        f"The contents of {HITS_LOG!r} do not match the expected initial "
        f"state.\nExpected ({len(EXPECTED_LINES)} lines):\n{EXPECTED_LINES}\n"
        f"Found ({len(lines)} lines):\n{lines}"
    )