# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# before the student performs any action.  It checks that:
#
# 1. The directory /home/user/net_logs exists.
# 2. The files /home/user/net_logs/ip_list.txt and
#    /home/user/net_logs/ping_ms.txt exist and contain the exact
#    expected contents (including trailing newlines).
# 3. The target output file /home/user/net_logs/summary.tsv does
#    NOT yet exist.
#
# Only Python’s stdlib and pytest are used.

import os
import pytest

BASE_DIR = "/home/user/net_logs"
IP_LIST_PATH = os.path.join(BASE_DIR, "ip_list.txt")
PING_MS_PATH = os.path.join(BASE_DIR, "ping_ms.txt")
SUMMARY_PATH = os.path.join(BASE_DIR, "summary.tsv")

IP_LIST_EXPECTED = [
    "192.168.0.1:80\n",
    "192.168.0.2:443\n",
    "10.0.0.1:22\n",
]

PING_MS_EXPECTED = [
    "32\n",
    "85\n",
    "12\n",
]


def test_net_logs_directory_exists():
    assert os.path.isdir(
        BASE_DIR
    ), f"Required directory {BASE_DIR} is missing."


@pytest.mark.parametrize(
    "path,expected_lines,description",
    [
        (IP_LIST_PATH, IP_LIST_EXPECTED, "ip_list.txt"),
        (PING_MS_PATH, PING_MS_EXPECTED, "ping_ms.txt"),
    ],
)
def test_source_files_exist_and_have_exact_contents(path, expected_lines, description):
    assert os.path.isfile(
        path
    ), f"Required file {path} ({description}) is missing."

    with open(path, "r", encoding="utf-8") as fh:
        contents = fh.readlines()

    assert contents == expected_lines, (
        f"{description} does not contain the expected contents.\n"
        f"Expected lines:\n{expected_lines!r}\n"
        f"Actual lines:\n{contents!r}"
    )


def test_summary_file_absent_initially():
    assert not os.path.exists(
        SUMMARY_PATH
    ), f"{SUMMARY_PATH} should NOT exist before the task is performed."