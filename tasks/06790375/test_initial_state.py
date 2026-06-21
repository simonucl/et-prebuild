# test_initial_state.py
#
# Pytest suite that validates the state of the operating system / filesystem
# *before* the student begins the exercise described in the prompt.
#
# The checks performed here assert ONLY the “starting” conditions that must
# already be true; they intentionally do NOT look for any artefacts that the
# student is supposed to create (e.g. the script or the log file).

from pathlib import Path
import pytest

HOME = Path("/home/user")
MICROSERVICES_DIR = HOME / "microservices"
SERVICES_FILE = MICROSERVICES_DIR / "services.txt"
SCRIPTS_DIR = HOME / "scripts"
REDEPLOY_SCRIPT = SCRIPTS_DIR / "redeploy_services.sh"
LOG_FILE = MICROSERVICES_DIR / "redeploy.log"

EXPECTED_SERVICE_LINES = ["auth", "api", "front"]


def test_microservices_directory_exists_and_is_directory():
    assert MICROSERVICES_DIR.exists(), (
        f"Required directory '{MICROSERVICES_DIR}' does not exist."
    )
    assert MICROSERVICES_DIR.is_dir(), (
        f"Path '{MICROSERVICES_DIR}' exists but is not a directory."
    )


def test_services_txt_exists_and_contents_are_correct():
    assert SERVICES_FILE.exists(), (
        f"Required file '{SERVICES_FILE}' does not exist."
    )
    assert SERVICES_FILE.is_file(), (
        f"Path '{SERVICES_FILE}' exists but is not a regular file."
    )

    raw_content = SERVICES_FILE.read_text(encoding="utf-8")
    lines = [line.rstrip("\n") for line in raw_content.splitlines()]

    assert lines == EXPECTED_SERVICE_LINES, (
        f"'{SERVICES_FILE}' contents are incorrect.\n"
        f"Expected exactly these lines: {EXPECTED_SERVICE_LINES}\n"
        f"Actual lines              : {lines}"
    )

    # Ensure every original line had a trailing newline (including the last one)
    assert raw_content.endswith("\n"), (
        f"Every line in '{SERVICES_FILE}' must end with a newline ('\\n')."
    )


def test_redeploy_script_does_not_exist_yet():
    assert not REDEPLOY_SCRIPT.exists(), (
        f"Script '{REDEPLOY_SCRIPT}' should NOT exist before the student starts."
    )


def test_redeploy_log_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"Log file '{LOG_FILE}' should NOT exist before the student starts."
    )