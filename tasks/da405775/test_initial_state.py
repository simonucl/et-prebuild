# test_initial_state.py
#
# Pytest suite that verifies the pre-task filesystem state for the
# “parallel YAML & TOML change” exercise.  These tests run *before*
# the student performs any actions, ensuring that the starting
# conditions are correct.
#
# Requirements verified:
#   • The two expected source files exist with their original contents.
#   • The required directories (/home/user/configs and /home/user/task_logs)
#     are present.
#   • No output artefacts (e.g. /home/user/task_logs/changes.log) exist yet.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import difflib
import pytest

# ---------------------------------------------------------------------------
# Constants – expected initial file contents (including the final newline)
# ---------------------------------------------------------------------------

API_GATEWAY_PATH = Path("/home/user/configs/api-gateway.yaml")
DB_SERVICE_PATH = Path("/home/user/configs/db-service.toml")
TASK_LOGS_DIR = Path("/home/user/task_logs")
CHANGE_LOG_PATH = TASK_LOGS_DIR / "changes.log"

EXPECTED_API_GATEWAY_CONTENT = (
    "server:\n"
    "  port: 8080\n"
    '  host: "0.0.0.0"\n'
    "logging:\n"
    '  level: "INFO"\n'
    "  enabled: false\n"
    "security:\n"
    "  cors:\n"
    "    allowed_origins:\n"
    '      - "https://example.com"\n'
    "    allow_credentials: false\n"
)

EXPECTED_DB_SERVICE_CONTENT = (
    "[database]\n"
    'host = "127.0.0.1"\n'
    "port = 5432\n"
    'username = "dbuser"\n'
    'password = "oldpassword"\n'
    "max_connections = 100\n"
    "\n"
    "[features]\n"
    "connection_pooling = true\n"
    "logging = false\n"
)

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _assert_contents(path: Path, expected: str):
    """
    Read `path` and assert that its byte-for-byte contents equal `expected`.
    On mismatch, produce a unified diff to help the learner.
    """
    assert path.exists(), f"Expected file {path} to exist."

    content = path.read_text(encoding="utf-8")
    if content != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                content.splitlines(),
                fromfile="expected",
                tofile=str(path),
                lineterm="",
            )
        )
        pytest.fail(
            f"Contents of {path} do not match the expected initial state:\n{diff}"
        )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_directories_exist():
    """Both /home/user/configs and /home/user/task_logs directories must exist."""
    configs_dir = Path("/home/user/configs")
    assert configs_dir.is_dir(), f"Directory {configs_dir} is missing."
    assert TASK_LOGS_DIR.is_dir(), f"Directory {TASK_LOGS_DIR} is missing."


def test_initial_files_exist_and_contents_are_correct():
    """The two configuration files should exist with their pristine contents."""
    _assert_contents(API_GATEWAY_PATH, EXPECTED_API_GATEWAY_CONTENT)
    _assert_contents(DB_SERVICE_PATH, EXPECTED_DB_SERVICE_CONTENT)


def test_no_output_files_yet():
    """
    The task log that the learner will create later must **not** exist before
    the exercise is started.
    """
    assert (
        not CHANGE_LOG_PATH.exists()
    ), f"Output file {CHANGE_LOG_PATH} should not exist before the task begins."