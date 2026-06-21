# test_initial_state.py
"""
Pytest suite validating the **initial** state of the operating system / file-system
_before_ the student performs the “ENV MANAGEMENT TASK”.

The checks guarantee that:
    • No dotenv or log file is present yet.
    • /home/user/.bashrc does NOT already contain the management block.
    • The relevant environment variables are not exported in the current shell.
"""

import os
from pathlib import Path
import pytest


APP_DIR = Path("/home/user/app")
DOTENV_FILE = APP_DIR / ".env"
LOG_FILE = APP_DIR / "env_setup.log"
BASHRC = Path("/home/user/.bashrc")

BEGIN_MARKER = "# BEGIN ENV MANAGEMENT TASK"
END_MARKER = "# END ENV MANAGEMENT TASK"


def _read_bashrc() -> str:
    """
    Helper – read the whole ~/.bashrc as text.
    If the file does not exist return an empty string.
    """
    try:
        return BASHRC.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def test_dotenv_file_absent():
    """
    The .env file must NOT exist before the task is executed.
    """
    assert not DOTENV_FILE.exists(), (
        "The dotenv file '/home/user/app/.env' already exists. "
        "The task says it should be created by the student."
    )


def test_log_file_absent():
    """
    The env_setup.log file must NOT exist before the task is executed.
    """
    assert not LOG_FILE.exists(), (
        "The log file '/home/user/app/env_setup.log' already exists. "
        "It should be generated only after the task is completed."
    )


def test_bashrc_has_no_management_block():
    """
    ~/.bashrc must NOT yet contain the ENV MANAGEMENT TASK block.
    """
    bashrc_content = _read_bashrc()
    assert BEGIN_MARKER not in bashrc_content, (
        f"Found '{BEGIN_MARKER}' in ~/.bashrc, "
        "but the student has not yet appended the block."
    )
    assert END_MARKER not in bashrc_content, (
        f"Found '{END_MARKER}' in ~/.bashrc, "
        "but the student has not yet appended the block."
    )


@pytest.mark.parametrize(
    "var_name",
    ["APP_ENV", "API_KEY", "DB_HOST", "DB_PORT"],
)
def test_env_vars_not_in_current_shell(var_name):
    """
    The variables must NOT yet be present in the current environment,
    because the sourcing logic has not been added/executed.
    """
    assert var_name not in os.environ, (
        f"Environment variable {var_name!r} is already set in this shell. "
        "It should become available only AFTER the student completes the task."
    )