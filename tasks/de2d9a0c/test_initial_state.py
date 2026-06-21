# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state that must be present **before** the student starts working on the
# “incident responder” task.  It confirms that the three source log files
# exist with the exact expected contents and that **no** output directory
# or summary file has been created yet.

import os
import pytest

HOME = "/home/user"
CLUSTER_LOG_DIR = os.path.join(HOME, "cluster_logs")
INCIDENT_DIR = os.path.join(HOME, "incident_report")
SUMMARY_FILE = os.path.join(INCIDENT_DIR, "summary.log")

EXPECTED_LOG_CONTENT = {
    "node1.log": [
        "INFO service started",
        "ERROR failed to connect db",
        "WARN retrying",
        "ERROR timeout",
    ],
    "node2.log": [
        "INFO service started",
        "INFO healthcheck pass",
        "INFO user login",
        "ERROR disk full",
        "ERROR disk full",
        "ERROR disk full",
    ],
    "node3.log": [
        "INFO service started",
        "WARN memory usage high",
        "INFO request processed",
    ],
}


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_LOG_CONTENT.items())
def test_cluster_log_files_exist_with_expected_content(filename, expected_lines):
    """
    Verify that each nodeX.log file exists under /home/user/cluster_logs/
    and contains exactly the expected content (both order and text).
    """
    full_path = os.path.join(CLUSTER_LOG_DIR, filename)

    # 1. File existence
    assert os.path.isfile(
        full_path
    ), f"Expected log file missing: {full_path!r}. " \
       "The task cannot proceed without this input."

    # 2. Exact content match (ignoring newline characters)
    with open(full_path, encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh.readlines()]

    assert actual_lines == expected_lines, (
        f"Content mismatch in {full_path!r}.\n"
        f"Expected lines ({len(expected_lines)}):\n{expected_lines}\n\n"
        f"Actual lines ({len(actual_lines)}):\n{actual_lines}"
    )


def test_incident_report_not_yet_created():
    """
    Before the student runs their solution, the /home/user/incident_report/
    directory and its summary file MUST NOT exist.
    """
    assert not os.path.exists(
        INCIDENT_DIR
    ), f"The output directory {INCIDENT_DIR!r} already exists, " \
       "but it should not be present before the task is attempted."

    assert not os.path.exists(
        SUMMARY_FILE
    ), f"The summary file {SUMMARY_FILE!r} already exists, " \
       "but it should not be present before the task is attempted."