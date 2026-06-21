# test_initial_state.py
#
# This pytest file validates the *initial* operating-system / filesystem
# state before the student performs any actions for the FinOps task.
#
# The checks performed are intentionally limited to the **input artefacts**
# that must already exist.  Per the project rules we do **not** touch or
# assert anything about the output paths that the student is expected to
# create later.
#
# Requirements verified:
#   • /home/user/finops/logs/cluster_usage.tsv exists and is a regular file
#   • The file content exactly matches the canonical ground-truth provided
#     by the test harness (line order, tab separation, trailing newline, etc.)

import os
import pytest

# ---------- Constants ---------- #
LOG_PATH = "/home/user/finops/logs/cluster_usage.tsv"

# The canonical ground-truth content of the usage log.  A final '\n' is kept
# on purpose because the file is expected to end with exactly one newline.
GROUND_TRUTH_CONTENT = (
    "2023-08-01T12:00:00Z\tcluster-a\tpayment\tapp-payment-api\tComputeHours\t50\t12.50\n"
    "2023-08-01T12:05:00Z\tcluster-b\tpayment\tapp-payment-api\tNetworkEgressGB\t30\t45.00\n"
    "2023-08-01T12:10:00Z\tcluster-a\tsearch\tapp-search-api\tComputeHours\t70\t20.00\n"
    "2023-08-01T12:15:00Z\tcluster-b\tsearch\tapp-search-api\tNetworkEgressGB\t10\t15.00\n"
    "2023-08-01T12:20:00Z\tcluster-c\tauth\tapp-auth-api\tComputeHours\t40\t8.00\n"
    "2023-08-01T12:25:00Z\tcluster-c\tauth\tapp-auth-api\tNetworkEgressGB\t5\t7.50\n"
    "2023-08-01T12:30:00Z\tcluster-a\treporting\tapp-report-api\tComputeHours\t100\t25.00\n"
    "2023-08-01T12:35:00Z\tcluster-b\treporting\tapp-report-api\tNetworkEgressGB\t120\t180.00\n"
    "2023-08-01T12:40:00Z\tcluster-a\tanalytics\tapp-analytics\tComputeHours\t80\t30.00\n"
    "2023-08-01T12:45:00Z\tcluster-b\tanalytics\tapp-analytics\tNetworkEgressGB\t60\t90.00\n"
)

EXPECTED_LINE_COUNT = 10
EXPECTED_COLUMN_COUNT = 7  # fixed by the task description


# ---------- Tests ---------- #
def test_usage_log_exists_and_is_file():
    """
    Verify that the usage log exists and is a regular file.
    """
    assert os.path.exists(LOG_PATH), (
        f"Expected usage log at '{LOG_PATH}' does not exist."
    )
    assert os.path.isfile(LOG_PATH), (
        f"Path '{LOG_PATH}' exists but is not a regular file."
    )


def test_usage_log_content_matches_ground_truth():
    """
    Ensure that the content of cluster_usage.tsv is exactly the ground truth
    provided by the exercise.  This protects students from working on an
    accidentally modified data set.
    """
    with open(LOG_PATH, "r", encoding="utf-8") as fp:
        content = fp.read()

    # 1) Full-string equality check for maximal strictness.
    assert content == GROUND_TRUTH_CONTENT, (
        "The content of the usage log does not match the expected ground truth."
    )

    # 2) Additional structural sanity checks (line and column counts).
    lines = [ln.rstrip("\n") for ln in content.splitlines()]
    assert len(lines) == EXPECTED_LINE_COUNT, (
        f"Expected {EXPECTED_LINE_COUNT} lines in the log file, "
        f"found {len(lines)}."
    )

    for idx, line in enumerate(lines, start=1):
        cols = line.split("\t")
        assert len(cols) == EXPECTED_COLUMN_COUNT, (
            f"Line {idx} in the usage log should have "
            f"{EXPECTED_COLUMN_COUNT} tab-separated columns, "
            f"but has {len(cols)} instead."
        )