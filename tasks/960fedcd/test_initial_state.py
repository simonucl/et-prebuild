# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem state
# before the student carries out the deployment-venv task.  These checks make
# sure that nothing has been pre-created and that the legacy project files are
# in place exactly as specified by the instructions.

from pathlib import Path
import pytest

# Fixed reference paths used throughout the tests
HOME_DIR = Path("/home/user")
PROJECT_DIR = HOME_DIR / "app"
REQUIREMENTS_FILE = PROJECT_DIR / "requirements.txt"
DEPLOY_VENV_DIR = PROJECT_DIR / "deploy_venv"
DEPLOY_LOGS_DIR = PROJECT_DIR / "deploy_logs"
UPGRADE_REPORT_FILE = DEPLOY_LOGS_DIR / "upgrade_report.log"


def test_project_directory_exists():
    """
    The project directory /home/user/app must already exist.  If this assertion
    fails, either the test runner is pointed at the wrong environment, or the
    initial project layout was not provided to the student.
    """
    assert PROJECT_DIR.is_dir(), (
        f"Expected project directory {PROJECT_DIR} to exist before the task "
        "begins, but it was not found."
    )


def test_requirements_file_contains_old_versions():
    """
    The historical requirements.txt file must exist and contain the older
    package versions (flask==2.2.0 and requests==2.28.0).  It should *not* yet
    contain the upgraded versions that the student is expected to install.
    """
    assert REQUIREMENTS_FILE.is_file(), (
        f"Expected {REQUIREMENTS_FILE} to exist, but it was missing."
    )

    contents = REQUIREMENTS_FILE.read_text().splitlines()

    expected_lines = {"flask==2.2.0", "requests==2.28.0"}
    missing = expected_lines - set(contents)
    assert not missing, (
        f"{REQUIREMENTS_FILE} is missing the following expected line(s): "
        f"{', '.join(sorted(missing))}"
    )

    # Guard against the upgraded versions already being present
    unwanted_lines = {"flask==2.3.2", "requests==2.31.0"}
    present_unwanted = unwanted_lines & set(contents)
    assert not present_unwanted, (
        f"{REQUIREMENTS_FILE} unexpectedly already contains upgraded version "
        f"line(s): {', '.join(sorted(present_unwanted))}. The file should "
        "reflect only the legacy versions at this stage."
    )


def test_deploy_venv_does_not_exist():
    """
    No virtual environment should exist prior to the student's commands.  Its
    presence would indicate that the grader is not starting from a clean slate.
    """
    assert not DEPLOY_VENV_DIR.exists(), (
        f"Virtual environment directory {DEPLOY_VENV_DIR} should *not* exist "
        "before the student creates it."
    )


def test_deploy_logs_directory_does_not_exist_or_is_empty_of_report():
    """
    The deploy_logs directory (and therefore the upgrade_report.log file) must
    be absent initially.  If the directory happens to exist for some unrelated
    reason, the upgrade_report.log file itself must still be absent.
    """
    if DEPLOY_LOGS_DIR.exists():
        # Directory exists; ensure the specific report file is not present.
        assert not UPGRADE_REPORT_FILE.exists(), (
            f"Found unexpected log file {UPGRADE_REPORT_FILE} before the task "
            "started.  The student should create it as part of their solution."
        )
    else:
        # Preferred state: directory is absent entirely.
        assert not DEPLOY_LOGS_DIR.exists(), (
            f"Directory {DEPLOY_LOGS_DIR} should not pre-exist; it must be "
            "created by the student."
        )