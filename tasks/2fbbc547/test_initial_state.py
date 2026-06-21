# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student runs any commands.  It asserts that only the
# demo project exists, that the .env file contains the expected
# AWS secret on line 3, and that the security_logs directory and its
# log file are *absent*.

import os
from pathlib import Path

PROJECT_DIR = Path("/home/user/project")
ENV_FILE = PROJECT_DIR / ".env"
SEC_LOG_DIR = Path("/home/user/security_logs")
SEC_LOG_FILE = SEC_LOG_DIR / "secret_scan.log"


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Expected directory {PROJECT_DIR} to exist, "
        "but it is missing."
    )


def test_project_files_exist():
    expected_files = ["README.md", ".env", "app.py"]
    missing = [f for f in expected_files if not (PROJECT_DIR / f).is_file()]
    assert not missing, (
        "The following expected files are missing from "
        f"{PROJECT_DIR}: {', '.join(missing)}"
    )


def test_env_file_contents():
    assert ENV_FILE.is_file(), f"Expected {ENV_FILE} to exist."
    # Read as binary to check for Windows line endings
    content = ENV_FILE.read_bytes()
    assert b"\r\n" not in content, (
        f"{ENV_FILE} contains Windows (CRLF) line endings; "
        "expected Unix (LF) endings."
    )

    lines = content.decode().splitlines()
    assert len(lines) == 3, (
        f"Expected {ENV_FILE} to have exactly 3 lines, "
        f"found {len(lines)}."
    )

    secret_lines = [
        (idx + 1, line) for idx, line in enumerate(lines)
        if "AWS_SECRET_ACCESS_KEY" in line
    ]
    assert secret_lines, (
        f"No line containing 'AWS_SECRET_ACCESS_KEY' found in {ENV_FILE}."
    )
    assert len(secret_lines) == 1, (
        f"Expected exactly one occurrence of 'AWS_SECRET_ACCESS_KEY' in "
        f"{ENV_FILE}, found {len(secret_lines)} occurrences."
    )
    line_no, line_text = secret_lines[0]
    assert line_no == 3, (
        f"'AWS_SECRET_ACCESS_KEY' should appear on line 3, "
        f"but was found on line {line_no}."
    )
    assert line_text.startswith("AWS_SECRET_ACCESS_KEY="), (
        f"The secret line should start with 'AWS_SECRET_ACCESS_KEY='; "
        f"got: {line_text!r}"
    )


def test_security_logs_absent_initially():
    assert not SEC_LOG_DIR.exists(), (
        f"Directory {SEC_LOG_DIR} should NOT exist before the "
        "student runs the solution."
    )
    assert not SEC_LOG_FILE.exists(), (
        f"File {SEC_LOG_FILE} should NOT exist before the "
        "student runs the solution."
    )