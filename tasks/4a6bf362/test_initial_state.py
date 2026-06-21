# test_initial_state.py
#
# This pytest suite validates the initial OS / filesystem state *before*
# the student begins working on the task.  It makes sure that:
#
# 1. The directory /home/user/server_logs/ exists and is writable by the user.
# 2. The expected *.log files exist.
# 3. Each log file contains exactly the lines specified in the task
#    description—no more, no less, and in the same order.
#
# NOTE:  Per the grading-suite requirements we deliberately *do not* check for
#        the presence (or absence) of the output file
#        /home/user/server_logs/status_summary.csv.
#
# Only stdlib + pytest are used.

import os
import stat
import textwrap
import pytest

SERVER_LOG_DIR = "/home/user/server_logs"

# --------------------------------------------------------------------------- #
# Helper data: expected contents for each log file in the exact order given.
# --------------------------------------------------------------------------- #
EXPECTED_LOG_CONTENTS = {
    "/home/user/server_logs/web01.log": textwrap.dedent(
        """\
        2023-06-01 00:00:01 status=UP
        2023-06-01 01:00:01 status=UP
        2023-06-01 02:00:01 status=UP
        2023-06-01 03:00:01 status=UP
        2023-06-01 04:00:01 status=UP
        2023-06-01 05:00:01 status=UP
        2023-06-01 06:00:01 status=UP
        2023-06-01 07:00:01 status=DOWN
        2023-06-01 08:00:01 status=DOWN
        2023-06-01 09:00:01 status=DOWN
        """
    ),
    "/home/user/server_logs/db01.log": textwrap.dedent(
        """\
        2023-06-01 00:30:01 status=UP
        2023-06-01 01:30:01 status=UP
        2023-06-01 02:30:01 status=UP
        2023-06-01 03:30:01 status=UP
        2023-06-01 04:30:01 status=UP
        2023-06-01 05:30:01 status=DOWN
        2023-06-01 06:30:01 status=DOWN
        2023-06-01 07:30:01 status=DOWN
        2023-06-01 08:30:01 status=DOWN
        2023-06-01 09:30:01 status=DOWN
        """
    ),
}

# Ensure every expected string ends with precisely one LF
EXPECTED_LOG_CONTENTS = {
    path: content.rstrip("\n") + "\n" for path, content in EXPECTED_LOG_CONTENTS.items()
}

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_log_directory_exists_and_writable():
    """Verify /home/user/server_logs exists and is writable by the current user."""
    assert os.path.isdir(
        SERVER_LOG_DIR
    ), "Directory /home/user/server_logs/ is missing or not a directory."

    st_mode = os.stat(SERVER_LOG_DIR).st_mode
    mode = stat.S_IMODE(st_mode)

    # 0o755 means: u=rwx,g=rx,o=rx.  We only insist that the
    # current user has rwx (0o700) and that the directory is at least executable for traversal.
    assert (
        mode & 0o700 == 0o700
    ), "Directory /home/user/server_logs/ does not have user read/write/execute permissions (expected 0755 or similar)."


@pytest.mark.parametrize("file_path", sorted(EXPECTED_LOG_CONTENTS.keys()))
def test_log_file_exists(file_path):
    """Each expected *.log file must exist."""
    assert os.path.isfile(
        file_path
    ), f"Expected log file {file_path} is missing."


@pytest.mark.parametrize("file_path,expected_content", sorted(EXPECTED_LOG_CONTENTS.items()))
def test_log_file_content_exact_match(file_path, expected_content):
    """The content of every log file must match exactly the specification."""
    with open(file_path, "r", encoding="utf-8") as fh:
        actual = fh.read()

    # For easier debugging on failure, give a short diff-like output.
    if actual != expected_content:
        # Show at most the first differing lines for brevity.
        expected_lines = expected_content.splitlines(keepends=True)
        actual_lines = actual.splitlines(keepends=True)
        prefix = []
        for exp, act in zip(expected_lines, actual_lines):
            if exp != act:
                prefix.append(f"EXPECTED: {exp!r}")
                prefix.append(f"ACTUAL  : {act!r}")
                break
        else:
            # One is a prefix of the other.
            prefix.append("One file has extra/missing lines.")
        diff_snippet = "\n".join(prefix)
        pytest.fail(
            f"Content mismatch in {file_path}.\n"
            f"--- Snippet of first difference ---\n{diff_snippet}"
        )