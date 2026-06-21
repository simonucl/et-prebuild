# test_initial_state.py
#
# This test-suite verifies that the starting filesystem state is exactly what
# the exercise description promises *before* the student performs any action.
#
# Checked pre-conditions:
# 1. /home/user/app/sample.env
#    - must exist as a file
#    - must contain three precise lines:
#        "# Sample configuration file\n"
#        "APP_ENV=development\n"
#        "RELEASE_TAG=dev\n"
# 2. /home/user/app/.env     must NOT exist yet
# 3. /home/user/deploy_summary.log  must NOT exist yet
#
# If any of these conditions fail, the student environment is already in an
# unexpected state and the remaining grading steps would be unreliable.

from pathlib import Path
import pytest

HOME = Path("/home/user")
APP_DIR = HOME / "app"
SAMPLE_ENV = APP_DIR / "sample.env"
ENV_FILE = APP_DIR / ".env"
SUMMARY_LOG = HOME / "deploy_summary.log"


def _read_file_lines(path: Path):
    """Read a text file and return its lines, preserving trailing newlines."""
    with path.open("r", encoding="utf-8") as f:
        return f.readlines()


@pytest.mark.describe("Verify initial project layout and content")
class TestInitialState:
    def test_sample_env_exists(self):
        assert SAMPLE_ENV.is_file(), (
            f"Expected '{SAMPLE_ENV}' to exist as a regular file, "
            "but it is missing."
        )

    def test_sample_env_content(self):
        expected_lines = [
            "# Sample configuration file\n",
            "APP_ENV=development\n",
            "RELEASE_TAG=dev\n",
        ]

        actual_lines = _read_file_lines(SAMPLE_ENV)
        assert actual_lines == expected_lines, (
            "The contents of 'sample.env' do not match the expected initial "
            "template.\n\n"
            f"Expected lines ({len(expected_lines)}):\n{''.join(expected_lines)!r}\n\n"
            f"Actual lines   ({len(actual_lines)}):\n{''.join(actual_lines)!r}"
        )

    def test_env_file_does_not_exist_yet(self):
        assert not ENV_FILE.exists(), (
            f"'{ENV_FILE}' should NOT exist before the student starts the task, "
            "but it is already present."
        )

    def test_deploy_summary_log_does_not_exist_yet(self):
        assert not SUMMARY_LOG.exists(), (
            f"'{SUMMARY_LOG}' should NOT exist before the student starts the task, "
            "but it is already present."
        )