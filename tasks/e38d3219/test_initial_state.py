# test_initial_state.py
#
# This test-suite validates that the sandbox is in the expected *initial*
# condition for the “daily roll-up CSV” exercise.  It purposefully checks
# only those artefacts that must be present **before** the student starts
# solving the task.
#
# IMPORTANT:  Per specification we must NOT touch or even mention any of
#             the output artefacts (/home/user/output/ …).  We therefore
#             restrict ourselves to the raw telemetry log.
#
# The tests assert that:
#   1. /home/user/logs/resource_usage_2023-08-04.log exists and is a file.
#   2. The file contains exactly the five expected lines, each terminated
#      with a single UNIX LF (“\n”).  No more, no less, no CR, no spaces.
#
# Any discrepancy will raise a descriptive assertion error so the learner
# immediately knows what prerequisite is missing or malformed.
#

from pathlib import Path

import pytest

# Absolute path to the required raw telemetry file
RAW_LOG = Path("/home/user/logs/resource_usage_2023-08-04.log")

# The byte-accurate content that MUST be present in RAW_LOG.
EXPECTED_CONTENT = (
    "2023-08-04 00:00:00 CPU=17% MEM=2048MB NET_IN=120kB/s NET_OUT=80kB/s\n"
    "2023-08-04 06:00:00 CPU=65% MEM=4096MB NET_IN=512kB/s NET_OUT=340kB/s\n"
    "2023-08-04 12:00:00 CPU=89% MEM=8192MB NET_IN=1024kB/s NET_OUT=840kB/s\n"
    "2023-08-04 18:00:00 CPU=4% MEM=1024MB NET_IN=12kB/s NET_OUT=8kB/s\n"
    "2023-08-04 23:59:59 CPU=52% MEM=6144MB NET_IN=256kB/s NET_OUT=210kB/s\n"
)


def test_raw_log_exists_and_is_file():
    """
    Verify that the raw telemetry log is present and is a regular file.
    """
    assert RAW_LOG.exists(), (
        f"Required telemetry file missing: {RAW_LOG}\n"
        "Without this file the exercise cannot be completed."
    )
    assert RAW_LOG.is_file(), (
        f"The path {RAW_LOG} exists but is not a regular file."
    )


def test_raw_log_contents_are_exact():
    """
    The file must contain the exact five lines documented in the spec,
    each terminated with a single LF.  This stringent check ensures the
    downstream solution can rely on stable input.
    """
    content = RAW_LOG.read_text(encoding="utf-8")

    # We perform two complementary checks so that failure messages are
    # as helpful as possible.
    assert content == EXPECTED_CONTENT, (
        "The contents of the raw telemetry file do not match the expected "
        "template.\n"
        "---------- Expected ----------\n"
        f"{EXPECTED_CONTENT!r}\n"
        "----------- Actual -----------\n"
        f"{content!r}\n"
        "--------------------------------\n"
        "Ensure the file has exactly five lines, each ending with a single "
        "newline character (\\n), and that every token matches the spec."
    )

    # Extra sanity: make sure there are exactly 5 lines
    lines = content.splitlines()
    assert len(lines) == 5, (
        f"Expected 5 lines in {RAW_LOG}, found {len(lines)} line(s)."
    )