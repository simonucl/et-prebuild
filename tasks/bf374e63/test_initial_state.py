# test_initial_state.py
#
# This pytest suite validates that the system is in a clean, predictable
# state *before* the student begins the capacity-planner exercise.
#
# It checks that none of the artefacts the student is supposed to create
# already exist, while ensuring that the supporting /home/user/reports
# directory (provided by the provisioning system) is present and writable.
#
# Only the Python stdlib and pytest are used.

import os
import stat
import pytest


CAPACITY_PLANNER_DIR = "/home/user/capacity_planner"
DOTENV_PATH = "/home/user/capacity_planner/.env"
SCRIPT_PATH = "/home/user/capacity_planner/analyze_usage.sh"
REPORTS_DIR = "/home/user/reports"
REPORT_LOG = "/home/user/reports/usage_report.log"
THRESHOLD_VARS = ("CPU_THRESHOLD", "MEM_THRESHOLD", "DISK_THRESHOLD")


def test_capacity_planner_directory_absent():
    """
    The workspace directory should NOT exist yet.
    The student will create /home/user/capacity_planner during the exercise.
    """
    assert not os.path.exists(
        CAPACITY_PLANNER_DIR
    ), "/home/user/capacity_planner should not exist before the student creates it."


def test_dotenv_file_absent():
    """
    The dotenv file (.env) must not pre-exist.
    """
    assert not os.path.exists(
        DOTENV_PATH
    ), ".env should not exist yet; the student will create it."


def test_analyze_usage_script_absent():
    """
    The reporting script must not pre-exist.
    """
    assert not os.path.exists(
        SCRIPT_PATH
    ), "analyze_usage.sh should not exist yet; the student will create it."


def test_report_log_absent():
    """
    The usage_report.log file should not exist until the student runs
    their script.
    """
    assert not os.path.exists(
        REPORT_LOG
    ), "usage_report.log should not exist before the student generates it."


def test_reports_directory_exists_and_is_writable():
    """
    The provisioning system must supply /home/user/reports and it must be
    writable so the student can append their report.
    """
    assert os.path.isdir(
        REPORTS_DIR
    ), "/home/user/reports directory is missing; it must exist for logging."
    assert os.access(
        REPORTS_DIR, os.W_OK
    ), "/home/user/reports exists but is not writable by the user."


def test_threshold_environment_variables_not_pre_set():
    """
    The threshold variables should not be pre-defined in the environment;
    the student script must read them from the .env file.
    """
    for var in THRESHOLD_VARS:
        assert var not in os.environ, (
            f"Environment variable {var} is already set; "
            "it should only come from the student's .env file."
        )