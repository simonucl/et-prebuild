# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state before the
# student rotates the exposed API credential.  It intentionally checks
# only the pre-condition assets and deliberately ignores any artefacts
# that are supposed to be created *after* the student’s work
# (e.g. /home/user/rotation_logs).

import os
from pathlib import Path

PROJECT_DIR = Path("/home/user/project")
ENV_FILE = PROJECT_DIR / ".env"

EXPECTED_ENV_LINES = [
    '# Application environment variables',
    'SERVICE_URL="https://dev.example.com"',
    'OLD_API_KEY="ABC123"',
    'DEBUG=true',
]


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Required directory {PROJECT_DIR} is missing.  "
        f"Create it before attempting credential rotation."
    )


def test_env_file_exists_and_has_expected_content():
    assert ENV_FILE.is_file(), (
        f"Expected file {ENV_FILE} does not exist."
    )

    # Read the file exactly as bytes and then decode; this preserves line endings.
    content = ENV_FILE.read_text(encoding="utf-8").splitlines()

    assert content == EXPECTED_ENV_LINES, (
        f"{ENV_FILE} does not contain the expected four-line content.\n"
        f"Expected:\n{os.linesep.join(EXPECTED_ENV_LINES)}\n\n"
        f"Found:\n{os.linesep.join(content)}"
    )


def test_old_key_still_present_before_rotation():
    # Ensure the exposed value is still present (this is the *before* state).
    with ENV_FILE.open(encoding="utf-8") as fh:
        data = fh.read()
    assert "ABC123" in data, (
        "The credential ABC123 was not found in .env; the pre-condition is wrong "
        "or someone has already modified the file."
    )
    assert "OLD_API_KEY" in data, (
        "Key name OLD_API_KEY missing; expected to find it before rotation."
    )
    # Ensure the replacement value is not yet present.
    assert "XYZ789" not in data, (
        "Found XYZ789 in the .env file before rotation; the file has already been changed."
    )