# test_initial_state.py
#
# This test-suite validates that the machine is in the expected “fresh”
# state *before* the student starts working on the exercise.  It checks:
#
# 1. The presence and permissions of /home/user/pipeline.
# 2. The existence and **exact** contents of /home/user/pipeline/app.log.
# 3. That no output file (/home/user/pipeline/error_summary.log) exists yet.
#
# Any failure message should guide the student toward what is missing or
# unexpectedly present.

import os
import stat
import pwd
import pytest

PIPELINE_DIR = "/home/user/pipeline"
APP_LOG = os.path.join(PIPELINE_DIR, "app.log")
OUTPUT_FILE = os.path.join(PIPELINE_DIR, "error_summary.log")

# The expected lines in app.log (Unix line endings, UTF-8).
EXPECTED_APP_LOG_LINES = [
    "[2023-11-10 10:01:02] INFO  Starting job",
    "[2023-11-10 10:01:03] ERROR [ERR1001] Failed to connect to DB",
    "[2023-11-10 10:01:04] WARN  Slow response",
    "[2023-11-10 10:01:05] ERROR [ERR1002] Timeout in service",
    "[2023-11-10 10:01:06] ERROR [ERR1001] Failed to connect to DB",
    "[2023-11-10 10:01:07] ERROR [ERR1003] Null pointer exception",
    "[2023-11-10 10:01:08] INFO  Job completed",
]


def test_pipeline_directory_exists_and_writable():
    assert os.path.isdir(PIPELINE_DIR), (
        f"Required directory {PIPELINE_DIR} is missing. "
        "Create it before proceeding."
    )

    # Verify owner has rwx permissions on the directory.
    stat_info = os.stat(PIPELINE_DIR)
    mode = stat.S_IMODE(stat_info.st_mode)
    # Owner permissions are the highest three bits of the octal mask.
    owner_perms = (mode & 0o700) >> 6
    expected_owner_perms = 0b111  # rwx
    assert (
        owner_perms & expected_owner_perms == expected_owner_perms
    ), (
        f"Directory {PIPELINE_DIR} should be owner-writable (rwx) "
        f"but has mode {oct(mode)}."
    )

    # Confirm it is owned by the current user for completeness.
    current_user = pwd.getpwuid(os.getuid()).pw_name
    dir_owner = pwd.getpwuid(stat_info.st_uid).pw_name
    assert (
        dir_owner == current_user
    ), f"{PIPELINE_DIR} must be owned by '{current_user}', found owner '{dir_owner}'."


def test_only_app_log_present_initially():
    entries = sorted(os.listdir(PIPELINE_DIR))
    assert "app.log" in entries, (
        f"{APP_LOG} is missing. It must already exist with the seed data."
    )
    # No other files except app.log should be present at the start.
    unexpected = [e for e in entries if e != "app.log"]
    assert not unexpected, (
        "Unexpected files/directories found in "
        f"{PIPELINE_DIR}: {', '.join(unexpected)}.  "
        "The directory should contain only app.log at the start."
    )


def test_app_log_contents_exact_match():
    assert os.path.isfile(APP_LOG), f"{APP_LOG} is missing or is not a file."

    with open(APP_LOG, "r", encoding="utf-8") as fh:
        contents = fh.read()

    # Normalize trailing newline: we'll allow the file to optionally end with \n.
    # Splitlines(keepends=False) discards the newline characters.
    lines = contents.splitlines()
    assert (
        lines == EXPECTED_APP_LOG_LINES
    ), (
        f"{APP_LOG} does not contain the expected seed data.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_APP_LOG_LINES)
        + "\n\nFound lines:\n"
        + "\n".join(lines)
    )


def test_output_file_absent_initially():
    assert not os.path.exists(
        OUTPUT_FILE
    ), f"{OUTPUT_FILE} should NOT exist before the exercise starts."