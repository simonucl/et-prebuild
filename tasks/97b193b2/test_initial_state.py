# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state *before* the student performs any action for the “status summary”
# task.  These tests assert that:
#
# 1. The source access-log file exists at the exact absolute path.
# 2. The access-log contains the expected eight lines.
# 3. The distribution of HTTP status codes inside the log matches the
#    specification (200→5, 302→1, 404→1, 500→1).
# 4. The destination report file does NOT exist yet (it will be created
#    by the student’s solution).
#
# Failures clearly indicate what is missing or incorrect.
#
# Only stdlib + pytest are used.

from pathlib import Path
import re
import pytest
from collections import Counter

ACCESS_LOG_PATH = Path("/home/user/projects/site/logs/access.log")
REPORT_FILE_PATH = Path("/home/user/projects/site/report/status_summary.log")

# ---------------------------------------------------------------------------

def test_access_log_file_exists():
    """
    The pre-generated Nginx access log must be present at the exact path
    given in the task description.
    """
    assert ACCESS_LOG_PATH.is_file(), (
        f"Expected access log at {ACCESS_LOG_PATH}, but the file is missing."
    )


def test_access_log_line_count():
    """
    Verify that the access log contains exactly eight lines as specified.
    """
    with ACCESS_LOG_PATH.open("r", encoding="utf-8") as fp:
        lines = fp.readlines()

    assert len(lines) == 8, (
        f"Expected 8 lines in {ACCESS_LOG_PATH}, found {len(lines)} lines instead."
    )


@pytest.mark.dependency(name="log_status_counts")
def test_access_log_status_code_distribution():
    """
    Parse the access log and confirm that the distribution of HTTP status
    codes matches the truth values provided in the task description.
    """
    expected_counts = {"200": 5, "302": 1, "404": 1, "500": 1}

    # Simple regex: the first group of three digits that follows the closing quote
    # of the request string.
    status_code_re = re.compile(r'"\s*(\d{3})\s')

    with ACCESS_LOG_PATH.open("r", encoding="utf-8") as fp:
        codes = []
        for lineno, line in enumerate(fp, 1):
            m = status_code_re.search(line)
            assert m, (
                f"Unable to parse status code on line {lineno} of "
                f"{ACCESS_LOG_PATH}:\n{line}"
            )
            codes.append(m.group(1))

    counts = Counter(codes)
    assert counts == expected_counts, (
        f"Status-code distribution in {ACCESS_LOG_PATH} is incorrect.\n"
        f"Expected: {expected_counts}\nFound:    {counts}"
    )


def test_report_file_does_not_exist_yet():
    """
    The status_summary.log report must NOT exist before the student runs
    their code.  Its presence would indicate that the environment is not
    in the expected initial state.
    """
    assert not REPORT_FILE_PATH.exists(), (
        f"{REPORT_FILE_PATH} already exists, but it should be created by "
        "the student's solution. Ensure the environment is clean before starting."
    )