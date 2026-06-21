# test_initial_state.py
"""
Pytest suite that validates the pristine environment *before* the student
begins the incident-response task for “inventory-app”.

The checks guarantee that:
1. All required files and directories exist with the expected hierarchy.
2. Configuration and status files contain the original PORT=4000 settings.
3. No incident log from a previous run is present.
4. Helper script is present and executable.

If any assertion fails, the accompanying message explains exactly what is
missing or out of specification.
"""

import os
import stat
import re
import pytest

HOME = "/home/user"
SERVICES_DIR = os.path.join(HOME, "services")
APP_DIR = os.path.join(SERVICES_DIR, "inventory-app")
CONFIG_DIR = os.path.join(APP_DIR, "config")
RUNTIME_DIR = os.path.join(APP_DIR, "runtime")
LOG_DIR = os.path.join(HOME, "incident_logs")

ENV_CONF = os.path.join(CONFIG_DIR, "env.conf")
SERVICE_STATUS = os.path.join(RUNTIME_DIR, "service.status")
MOCK_SCRIPT = os.path.join(APP_DIR, "mock_service.sh")
INCIDENT_LOG = os.path.join(LOG_DIR, "inventory_fix.log")

EXPECTED_ENV_CONTENT = "APP_ENV=production\nPORT=4000\n"
EXPECTED_STATUS_CONTENT = "running on 4000\n"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def assert_file_mode(path: str, expected_mode: int) -> None:
    """Assert that `path` has permissions `expected_mode` (e.g. 0o755)."""
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert mode == expected_mode, (
        f"Expected file mode {oct(expected_mode)} for {path}, "
        f"but found {oct(mode)}"
    )


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# Directory existence tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path",
    [
        SERVICES_DIR,
        APP_DIR,
        CONFIG_DIR,
        RUNTIME_DIR,
        LOG_DIR,
    ],
)
def test_directories_exist(path):
    assert os.path.isdir(path), f"Required directory does not exist: {path}"
    # All directories should be world-readable/executable (0o755)
    assert_file_mode(path, 0o755)


# --------------------------------------------------------------------------- #
# File existence & permissions
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path",
    [
        ENV_CONF,
        SERVICE_STATUS,
        MOCK_SCRIPT,
    ],
)
def test_files_exist(path):
    assert os.path.isfile(path), f"Required file does not exist: {path}"
    # All version-controlled files should be 0o755 if executable else 0o644
    expected_mode = 0o755 if path == MOCK_SCRIPT else 0o644
    assert_file_mode(path, expected_mode)


def test_mock_service_is_executable():
    """mock_service.sh must be executable so the student can run it."""
    assert os.access(
        MOCK_SCRIPT, os.X_OK
    ), f"{MOCK_SCRIPT} is not executable (missing +x permission)"


# --------------------------------------------------------------------------- #
# Initial contents of env.conf
# --------------------------------------------------------------------------- #
def test_env_conf_initial_contents():
    content = read_text(ENV_CONF)
    assert (
        content == EXPECTED_ENV_CONTENT
    ), f"{ENV_CONF} content mismatch:\nExpected:\n{EXPECTED_ENV_CONTENT!r}\nGot:\n{content!r}"
    assert "PORT=4500" not in content, (
        f"{ENV_CONF} already contains PORT=4500; "
        "the student must change it from 4000 to 4500 during the task."
    )


# --------------------------------------------------------------------------- #
# Initial contents of service.status
# --------------------------------------------------------------------------- #
def test_service_status_initial_contents():
    content = read_text(SERVICE_STATUS)
    assert (
        content == EXPECTED_STATUS_CONTENT
    ), f"{SERVICE_STATUS} content mismatch:\nExpected:\n{EXPECTED_STATUS_CONTENT!r}\nGot:\n{content!r}"


# --------------------------------------------------------------------------- #
# Incident log must not pre-exist
# --------------------------------------------------------------------------- #
def test_incident_log_does_not_exist():
    assert not os.path.exists(
        INCIDENT_LOG
    ), f"Incident log {INCIDENT_LOG} already exists; the environment should be pristine."


# --------------------------------------------------------------------------- #
# Sanity check: incident_logs directory is empty
# --------------------------------------------------------------------------- #
def test_incident_logs_dir_is_empty():
    files = os.listdir(LOG_DIR)
    assert (
        files == [] or files == [".gitkeep"]
    ), f"{LOG_DIR} should be empty before the task begins (found {files})."


# --------------------------------------------------------------------------- #
# Optional: sanity regex checks on env.conf & status lines
# --------------------------------------------------------------------------- #
def test_env_conf_has_two_lines_only():
    lines = read_text(ENV_CONF).splitlines()
    assert len(lines) == 2, f"{ENV_CONF} should contain exactly two lines."


def test_status_file_format():
    pattern = r"^running on \d+\n$"
    content = read_text(SERVICE_STATUS)
    assert re.fullmatch(
        pattern, content
    ), f"{SERVICE_STATUS} format invalid, expected 'running on <PORT>' with newline."