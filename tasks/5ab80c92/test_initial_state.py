# test_initial_state.py
#
# This test-suite validates that the machine is in the *initial* state
# expected *before* the student performs any actions for the “webapp
# port-migration” exercise.

import os
import stat
import subprocess
import re
import pytest

HOME = "/home/user"
WEBAPP_DIR = os.path.join(HOME, "services", "webapp")
CONF_FILE = os.path.join(WEBAPP_DIR, "app.conf")
RESTART_SCRIPT = os.path.join(WEBAPP_DIR, "restart.sh")
INCIDENT_DIR = os.path.join(HOME, "incident_logs")


def test_webapp_directory_exists():
    assert os.path.isdir(WEBAPP_DIR), (
        f"Expected webapp directory '{WEBAPP_DIR}' to exist."
    )


def test_app_conf_initial_contents():
    assert os.path.isfile(CONF_FILE), f"Config file '{CONF_FILE}' is missing."

    with open(CONF_FILE, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Strip trailing newline for comparison but still verify newline count
    stripped = [ln.rstrip("\n") for ln in lines]

    assert stripped == ["PORT=8080", "DEBUG=False"], (
        "Config file should contain exactly two lines:\n"
        "PORT=8080\nDEBUG=False\n"
        f"Found:\n{''.join(lines)}"
    )

    # Ensure the file ends with a newline character
    assert lines[-1].endswith("\n"), "The last line of app.conf must end with a newline."


def test_restart_script_exists_and_is_executable():
    assert os.path.isfile(RESTART_SCRIPT), f"Restart script '{RESTART_SCRIPT}' is missing."

    st = os.stat(RESTART_SCRIPT)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Restart script '{RESTART_SCRIPT}' must have the executable flag set."


def test_restart_script_reports_port_8080():
    """The helper script should report port 8080 in the initial state."""
    completed = subprocess.run(
        [RESTART_SCRIPT],
        check=True,
        capture_output=True,
        text=True,
    )
    expected_output = "Webapp restarted on port 8080\n"
    assert completed.stdout == expected_output, (
        "In the initial state, restart.sh should report:\n"
        f"{expected_output!r}\n"
        f"Got:\n{completed.stdout!r}"
    )


def test_incident_logs_directory_absent():
    assert not os.path.exists(
        INCIDENT_DIR
    ), f"Directory '{INCIDENT_DIR}' should NOT exist before the task is started."


def test_no_incident_log_file_present():
    """Guard against pre-existing log files anywhere under /home/user/incident_logs."""
    if os.path.isdir(INCIDENT_DIR):
        # If the directory exists (it shouldn't), ensure it is empty.
        contents = os.listdir(INCIDENT_DIR)
        assert not contents, (
            f"Directory '{INCIDENT_DIR}' must be empty, but contains: {contents}"
        )


def test_no_rogue_incident_files_elsewhere():
    """Ensure no one created the final log file in the wrong location."""
    forbidden_path = os.path.join(HOME, "2023-incident-0001.log")
    assert not os.path.exists(forbidden_path), (
        f"Incident log file should NOT exist at '{forbidden_path}'."
    )