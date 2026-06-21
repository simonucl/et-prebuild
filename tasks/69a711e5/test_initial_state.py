# test_initial_state.py
#
# This test-suite verifies the **initial** filesystem state that must be
# present *before* the student begins working on the task.  It asserts
# that only the scaffold files/directories exist and that none of the
# artefacts the student is asked to create are present yet.
#
# Requirements being checked:
#
# 1.  /home/user/app/……………… directory scaffold exists.
# 2.  /home/user/app/.env.sample exists and is readable (the only file that
#     should exist prior to the task).
# 3.  /home/user/app/.env does **NOT** exist yet.
# 4.  /home/user/app/logs directory does **NOT** exist yet.
# 5.  /home/user/app/logs/env_debug.log does **NOT** exist yet.
#
# If any of these assertions fail, the error message will clearly state
# what is missing or what should not be there.

from pathlib import Path
import os
import stat
import pytest


APP_ROOT = Path("/home/user/app")
ENV_SAMPLE = APP_ROOT / ".env.sample"
ENV_FILE = APP_ROOT / ".env"
LOGS_DIR = APP_ROOT / "logs"
ENV_LOG = LOGS_DIR / "env_debug.log"


def test_app_root_exists_and_is_dir():
    assert APP_ROOT.exists(), (
        "The directory '/home/user/app' is missing. "
        "It should be provided in the starter repository."
    )
    assert APP_ROOT.is_dir(), (
        f"'{APP_ROOT}' exists but is not a directory. "
        "A directory is required as project root."
    )


def test_env_sample_exists_and_non_empty():
    assert ENV_SAMPLE.exists(), (
        "The scaffold file '/home/user/app/.env.sample' is missing. "
        "It should be present before the student starts the task."
    )
    assert ENV_SAMPLE.is_file(), (
        f"'{ENV_SAMPLE}' exists but is not a regular file."
    )
    size = ENV_SAMPLE.stat().st_size
    assert size > 0, (
        f"'{ENV_SAMPLE}' is empty; it should contain placeholder content."
    )


def test_env_file_does_not_exist_yet():
    assert not ENV_FILE.exists(), (
        "The file '/home/user/app/.env' already exists, "
        "but it should be created by the student, not beforehand."
    )


def test_logs_dir_does_not_exist_yet():
    assert not LOGS_DIR.exists(), (
        "The directory '/home/user/app/logs' already exists, "
        "but it should be created by the student, not beforehand."
    )


def test_env_log_file_does_not_exist_yet():
    assert not ENV_LOG.exists(), (
        "The file '/home/user/app/logs/env_debug.log' already exists, "
        "but it should be created by the student, not beforehand."
    )