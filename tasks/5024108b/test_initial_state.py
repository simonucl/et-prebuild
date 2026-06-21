# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem / OS state
# before the student starts working on the “artifact-repository” task.
#
# What we expect *to be present*:
#   • /home/user/logs/artifact_audit.log              (0644, exact content)
#   • /home/user/logs                                 (a directory)
#
# What we expect *NOT* to be present *yet*:
#   • /home/user/reports/                             (directory)
#   • /home/user/reports/bad_requests.log             (file)
#   • /home/user/reports/bad_request_summary.txt      (file)
#
# Failing tests clearly explain what is wrong / missing.
#
# Only stdlib + pytest is used.

import os
import stat
import pytest

LOG_DIR            = "/home/user/logs"
LOG_FILE           = "/home/user/logs/artifact_audit.log"
REPORTS_DIR        = "/home/user/reports"
BAD_REQ_LOG        = "/home/user/reports/bad_requests.log"
BAD_REQ_SUMMARY    = "/home/user/reports/bad_request_summary.txt"

EXPECTED_LOG_LINES = [
    "2024-07-20T10:15:42Z repo-core/org/example/libfoo-1.2.3.jar 200 -\n",
    "2024-07-20T10:15:43Z repo-core/org/example/libbar-2.0.0.jar 404 Not Found\n",
    "2024-07-20T10:16:01Z repo-proprietary/com/acme/widget-5.1.0.bin 500 Internal Server Error\n",
    "2024-07-20T10:16:05Z repo-proprietary/com/acme/widget-5.1.0.sig 200 -\n",
    "2024-07-20T10:17:22Z repo-dev/io/experiment/test-0.0.1-alpha.jar 404 Not Found\n",
    "2024-07-20T10:18:55Z repo-core/org/example/libbaz-3.1.4.jar 200 -\n",
    "2024-07-20T10:19:04Z repo-core/org/example/libbar-2.0.0-sources.jar 404 Not Found\n",
]

# --------------------------------------------------------------------------- #
# Positive assertions: things that must already exist
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR} is missing. "
        "The raw HTTP access log must reside in this directory."
    )

def test_log_file_exists_and_is_regular():
    assert os.path.isfile(LOG_FILE), f"Required log file {LOG_FILE} is missing."
    mode = os.stat(LOG_FILE).st_mode
    assert stat.S_ISREG(mode), f"{LOG_FILE} exists but is not a regular file."

def test_log_file_permissions_0644():
    perms = stat.S_IMODE(os.stat(LOG_FILE).st_mode)
    assert perms == 0o644, (
        f"{LOG_FILE} must have permissions 0644, found {oct(perms)}."
    )

def test_log_file_exact_content():
    """
    The grader relies on the exact, byte-for-byte content of artifact_audit.log.
    Make sure no extra/changed lines slipped in.
    """
    with open(LOG_FILE, "r", newline="") as fh:
        lines = fh.readlines()

    # Helpful diff if the content differs
    assert lines == EXPECTED_LOG_LINES, (
        f"{LOG_FILE} content does not match the expected initial fixture.\n"
        "Differences:\n"
        f"EXPECTED ({len(EXPECTED_LOG_LINES)} lines):\n{''.join(EXPECTED_LOG_LINES)}\n"
        f"FOUND    ({len(lines)} lines):\n{''.join(lines)}"
    )

# --------------------------------------------------------------------------- #
# Negative assertions: artefacts that must NOT exist yet
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path,kind",
    [
        (REPORTS_DIR, "directory"),
        (BAD_REQ_LOG, "file"),
        (BAD_REQ_SUMMARY, "file"),
    ],
)
def test_reports_outputs_do_not_yet_exist(path, kind):
    assert not os.path.exists(path), (
        f"{kind.capitalize()} {path} already exists, but it should be created "
        "by the student’s solution script, not beforehand."
    )