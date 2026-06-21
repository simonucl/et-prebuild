# test_initial_state.py
#
# This pytest file validates the initial state of the filesystem
# before the student performs any action.  It checks that
# /home/user/device_deploy.log exists with the expected permissions,
# expected number of lines, and the correct number of “[ERROR]”
# occurrences.  It deliberately does NOT test for the output file
# (/home/user/error_count.log), in accordance with the grading rules.

import os
import stat
import re
import pytest

DEVICE_LOG = "/home/user/device_deploy.log"

EXPECTED_LINES = [
    "2023-10-01 10:00:00 [INFO]  Deployment started",
    "2023-10-01 10:01:00 [ERROR] Connection timeout",
    "2023-10-01 10:02:00 [INFO]  Retrying deployment",
    "2023-10-01 10:03:00 [ERROR] Authentication failed",
    "2023-10-01 10:04:00 [INFO]  Deployment aborted",
    "2023-10-01 10:05:00 [ERROR] Rollback failed",
    "2023-10-01 10:06:00 [INFO]  Support notified",
]

ERROR_TAG = "[ERROR]"
EXPECTED_ERROR_COUNT = 3


@pytest.fixture(scope="module")
def device_log_contents():
    """
    Reads the entire log file once and returns a list of lines (stripped of
    trailing newlines) for downstream tests.
    """
    if not os.path.exists(DEVICE_LOG):
        pytest.skip(f"{DEVICE_LOG} does not exist on this system.")
    with open(DEVICE_LOG, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()]


def test_device_log_exists():
    assert os.path.isfile(DEVICE_LOG), (
        f"Expected {DEVICE_LOG} to be a regular file, but it does not exist "
        "or is not a file."
    )


def test_device_log_permissions():
    file_mode = stat.S_IMODE(os.stat(DEVICE_LOG).st_mode)
    expected_mode = 0o644
    assert (
        file_mode == expected_mode
    ), f"{DEVICE_LOG} should have permissions 644, found {oct(file_mode)}."


def test_device_log_line_count(device_log_contents):
    assert len(device_log_contents) == 7, (
        f"{DEVICE_LOG} should contain exactly 7 lines, "
        f"found {len(device_log_contents)}."
    )


def test_device_log_exact_content(device_log_contents):
    # Verify each line exactly matches the expected text.
    mismatches = [
        (idx + 1, exp, act)
        for idx, (exp, act) in enumerate(zip(EXPECTED_LINES, device_log_contents))
        if exp != act
    ]
    assert not mismatches, (
        "Content mismatch found in device_deploy.log:\n"
        + "\n".join(
            f"Line {ln}: expected '{exp}' but found '{act}'"
            for ln, exp, act in mismatches
        )
    )


def test_error_tag_occurrences(device_log_contents):
    error_lines = [ln for ln in device_log_contents if ERROR_TAG in ln]
    assert len(error_lines) == EXPECTED_ERROR_COUNT, (
        f"Expected {EXPECTED_ERROR_COUNT} lines containing '{ERROR_TAG}', "
        f"but found {len(error_lines)}."
    )
    # Additional check: ensure the tag appears once per error line (no duplicates)
    for ln in error_lines:
        occurrences = len(re.findall(re.escape(ERROR_TAG), ln))
        assert occurrences == 1, (
            f"Line '{ln}' should contain exactly one occurrence of '{ERROR_TAG}', "
            f"found {occurrences}."
        )