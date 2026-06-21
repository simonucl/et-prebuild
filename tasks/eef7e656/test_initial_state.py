# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student runs any commands.  It must PASS **untouched**;
# if it fails, the exercise has been started in an unexpected state.

from pathlib import Path
import pytest

# Constant paths
LOG_DIR = Path("/home/user/logs")
SYSLOG_SAMPLE = LOG_DIR / "syslog_sample.log"
FILTERED_SYSLOG = LOG_DIR / "filtered_syslog.log"
SUMMARY_LOG = LOG_DIR / "summary.log"

# Expected contents of the initial sample file (each string ends with '\n')
EXPECTED_SYSLOG_LINES = [
    "2023-08-25 10:02:15 server1 sshd[1234]: INFO User root logged in\n",
    "2023-08-25 10:03:10 server1 sshd[1234]: WARN Failed password attempt for user dev\n",
    "2023-08-25 10:05:42 server1 app[5678]: ERROR Could not connect to database [code=DBCONN01]\n",
    "2023-08-25 10:06:00 server1 kernel: INFO CPU temperature normal\n",
    "2023-08-25 10:07:18 server1 app[5678]: ERROR Timeout while reading socket [code=SOCKTIME02]\n",
    "2023-08-25 10:08:22 server1 app[5678]: WARN Deprecated API usage detected\n",
    "2023-08-25 10:09:30 server1 backup[9012]: INFO Backup completed successfully\n",
]


def test_log_directory_exists_and_is_directory():
    """The /home/user/logs directory must exist and be a directory."""
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} to exist."
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory."


def test_syslog_sample_exists_and_contents_are_correct():
    """Validate that syslog_sample.log exists with the exact expected content."""
    assert SYSLOG_SAMPLE.exists(), f"Missing required file: {SYSLOG_SAMPLE}"
    assert SYSLOG_SAMPLE.is_file(), f"{SYSLOG_SAMPLE} exists but is not a regular file."

    # Read the contents and compare line-by-line (including trailing newlines)
    with SYSLOG_SAMPLE.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == EXPECTED_SYSLOG_LINES, (
        "Contents of syslog_sample.log do not match the expected test fixture.\n"
        f"Expected lines ({len(EXPECTED_SYSLOG_LINES)}):\n{''.join(EXPECTED_SYSLOG_LINES)}\n"
        f"Actual lines ({len(actual_lines)}):\n{''.join(actual_lines)}"
    )


@pytest.mark.parametrize("path_to_check", [FILTERED_SYSLOG, SUMMARY_LOG])
def test_output_files_do_not_yet_exist(path_to_check):
    """The artifacts to be created by the student must NOT exist at the start."""
    assert not path_to_check.exists(), (
        f"File {path_to_check} already exists. Initial state should NOT contain "
        f"any generated artifacts."
    )


def test_no_extra_files_in_logs_directory():
    """
    Apart from syslog_sample.log, no other non-hidden files should be present
    in /home/user/logs/ at the outset.
    """
    non_hidden_files = sorted(
        p.name for p in LOG_DIR.iterdir() if p.is_file() and not p.name.startswith(".")
    )
    assert non_hidden_files == ["syslog_sample.log"], (
        f"Unexpected files found in {LOG_DIR}: {non_hidden_files}. "
        "Only 'syslog_sample.log' should be present before the task begins."
    )