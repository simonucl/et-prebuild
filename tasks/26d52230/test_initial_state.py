# test_initial_state.py
#
# Pytest suite that validates the operating-system state
# BEFORE the student runs their single-command solution.
#
# Rules & rationale:
#   • Only checks **pre-existing** artefacts.
#   • Never touches or tests any “output” path (/home/user/output …).
#   • Gives crystal-clear failure messages so the learner immediately
#     knows which prerequisite is missing or malformed.
#
# Tested prerequisites:
#   1. /home/user/logs/ directory exists.
#   2. /home/user/logs/sys_events.log file exists.
#   3. The log file contains EXACTLY the eight expected lines,
#      each ending in a single LF.
#   4. Exactly four lines contain “[ERROR]” or “[CRITICAL]”.
#
# Only standard library + pytest is used.

import os
import pathlib
import pytest

LOG_DIR = pathlib.Path("/home/user/logs")
LOG_FILE = LOG_DIR / "sys_events.log"

EXPECTED_LINES = [
    "2023-06-01 10:15:23 [INFO] Application started\n",
    "2023-06-01 10:15:24 [ERROR] Failed to open config file\n",
    "2023-06-01 10:15:25 [WARNING] Low memory\n",
    "2023-06-01 10:15:26 [ERROR] Failed to connect to database\n",
    "2023-06-01 10:15:27 [INFO] Retrying connection\n",
    "2023-06-01 10:15:28 [CRITICAL] System crash\n",
    "2023-06-01 10:15:29 [ERROR] Data corruption detected\n",
    "2023-06-01 10:15:30 [INFO] Shutdown sequence initiated\n",
]


def test_log_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Required directory {LOG_DIR} is missing. "
        "Create it before proceeding."
    )


def test_sys_events_log_exists():
    assert LOG_FILE.is_file(), (
        f"Required log file {LOG_FILE} is missing. "
        "It must exist before running your command."
    )


def test_sys_events_log_contents_exact_match():
    with LOG_FILE.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == EXPECTED_LINES, (
        "The contents of sys_events.log are not exactly as expected.\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n{''.join(EXPECTED_LINES)}\n"
        f"Got ({len(actual_lines)} lines):\n{''.join(actual_lines)}"
    )


def test_error_and_critical_line_count_is_four():
    with LOG_FILE.open("r", encoding="utf-8") as fh:
        hit_lines = [ln for ln in fh if "[ERROR]" in ln or "[CRITICAL]" in ln]

    assert len(hit_lines) == 4, (
        "Pre-check failed: there should be exactly 4 lines containing "
        "[ERROR] or [CRITICAL] in sys_events.log, "
        f"but found {len(hit_lines)}."
    )