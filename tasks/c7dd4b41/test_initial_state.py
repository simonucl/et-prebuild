# test_initial_state.py
#
# This test-suite validates the repository *before* the student makes any
# changes.  It asserts that:
#
# 1. /home/user/app exists and contains a Dockerfile with the exact, original
#    three-line content required by the exercise.
# 2. /home/user/policy does **not** yet exist.
#
# Only stdlib + pytest is used.

import os
import stat
import pytest
from pathlib import Path


APP_DIR = Path("/home/user/app")
DOCKERFILE = APP_DIR / "Dockerfile"
POLICY_DIR = Path("/home/user/policy")

# Expected, **exact** content of the original Dockerfile, including newlines.
EXPECTED_DOCKERFILE_CONTENT = (
    "FROM alpine:latest\n"
    "\n"
    "CMD [\"echo\", \"Hello World\"]\n"
)


def test_app_directory_exists():
    assert APP_DIR.is_dir(), (
        f"Required directory {APP_DIR} does not exist. The exercise expects the "
        "directory to be present before any edits are made."
    )


def test_dockerfile_exists_and_readable():
    assert DOCKERFILE.is_file(), (
        f"Required file {DOCKERFILE} is missing. It must exist before the student "
        "starts the task."
    )
    # World-readable means the 'other' read bit is set.
    file_mode = DOCKERFILE.stat().st_mode
    is_world_readable = bool(file_mode & stat.S_IROTH)
    assert is_world_readable, (
        f"{DOCKERFILE} must be world-readable so the automated tests can read it."
    )


def test_dockerfile_initial_content():
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert content == EXPECTED_DOCKERFILE_CONTENT, (
        f"{DOCKERFILE} does not contain the expected pre-exercise content.\n"
        "---- Expected ----\n"
        f"{EXPECTED_DOCKERFILE_CONTENT!r}\n"
        "---- Found ----\n"
        f"{content!r}\n"
        "The student must start from the exact original file."
    )


def test_policy_directory_absent_initially():
    assert not POLICY_DIR.exists(), (
        f"The directory {POLICY_DIR} should NOT exist prior to the student's "
        "actions. The test expects it to be created by the student."
    )