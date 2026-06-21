# test_initial_state.py
#
# This test-suite validates the **initial** state of the filesystem
# *before* the student starts solving the exercise.  It checks that
# the pre-existing log file is present and correct, and that none of
# the files the student is supposed to create already exist.

import os
import stat
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
SERVER_LOG = os.path.join(DATA_DIR, "server.log")

# Files that must *not* exist before the student starts working
OUTPUT_SCRIPT = os.path.join(DATA_DIR, "extract_cf.sh")
CRIT_FATAL_LOG = os.path.join(DATA_DIR, "critical_fatal.log")
SUMMARY_FILE = os.path.join(DATA_DIR, "summary.txt")


@pytest.fixture(scope="module")
def server_log_lines():
    """Return the content (as a list of stripped lines) of server.log."""
    if not os.path.isfile(SERVER_LOG):
        pytest.fail(
            f"Pre-existing log file missing: '{SERVER_LOG}' was not found."
        )
    with open(SERVER_LOG, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


def test_data_directory_exists():
    assert os.path.isdir(DATA_DIR), (
        f"Required directory '{DATA_DIR}' is missing."
    )


def test_server_log_exists_and_is_regular_file():
    assert os.path.isfile(SERVER_LOG), (
        f"Required file '{SERVER_LOG}' is missing."
    )
    file_mode = os.stat(SERVER_LOG).st_mode
    assert stat.S_ISREG(file_mode), (
        f"'{SERVER_LOG}' exists but is not a regular file."
    )


def test_server_log_has_expected_number_of_lines(server_log_lines):
    expected_line_count = 10
    assert len(server_log_lines) == expected_line_count, (
        f"'{SERVER_LOG}' should contain exactly {expected_line_count} lines; "
        f"found {len(server_log_lines)}."
    )


def test_server_log_contains_expected_tokens(server_log_lines):
    critical_lines = [ln for ln in server_log_lines if "[CRITICAL]" in ln]
    fatal_lines = [ln for ln in server_log_lines if "[FATAL]" in ln]

    assert len(critical_lines) == 2, (
        f"Expected 2 lines containing '[CRITICAL]' in '{SERVER_LOG}', "
        f"found {len(critical_lines)}."
    )
    assert len(fatal_lines) == 2, (
        f"Expected 2 lines containing '[FATAL]' in '{SERVER_LOG}', "
        f"found {len(fatal_lines)}."
    )

    # Ensure that the four lines appear in the original order
    combined = critical_lines + fatal_lines
    indices = [server_log_lines.index(ln) for ln in combined]
    assert indices == sorted(indices), (
        "Lines containing '[CRITICAL]' or '[FATAL]' are not in the expected "
        "order inside server.log."
    )


@pytest.mark.parametrize(
    "path",
    [OUTPUT_SCRIPT, CRIT_FATAL_LOG, SUMMARY_FILE],
)
def test_solution_files_do_not_exist_yet(path):
    assert not os.path.exists(path), (
        f"File '{path}' should NOT exist before the student starts working."
    )