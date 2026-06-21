# test_initial_state.py
#
# Pytest suite that validates the initial state of the repository *before*
# the student writes any solution code.  It checks only the pre-existing
# project files and never inspects the output artefacts (e.g. /home/user/scan_logs).
#
# Rules enforced:
#   • /home/user/app/ exists with sub-dirs service-a/ and service-b/
#   • Each sub-directory contains a Dockerfile.
#   • The contents of the two Dockerfiles are exactly as specified.
#
# If any check fails, the assertion message pin-points the problem so the
# student (or the autograder author) can immediately see what is wrong.
#
# NOTE: All paths are absolute, as required, and we purposely avoid looking
#       for any files that the student is expected to create later.

from pathlib import Path
import pytest

# --------------------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------------------
APP_DIR = Path("/home/user/app")
SERVICE_A_DIR = APP_DIR / "service-a"
SERVICE_B_DIR = APP_DIR / "service-b"
SERVICE_A_DOCKERFILE = SERVICE_A_DIR / "Dockerfile"
SERVICE_B_DOCKERFILE = SERVICE_B_DIR / "Dockerfile"

EXPECTED_CONTENT_SERVICE_A = [
    "FROM python:3.10-slim",
    "COPY . /app",
    "RUN pip install -r requirements.txt",
]

EXPECTED_CONTENT_SERVICE_B = [
    "FROM node:18",
    "ADD . /usr/src/app",
    "RUN npm install",
]

# --------------------------------------------------------------------------------------
# HELPER
# --------------------------------------------------------------------------------------
def read_dockerfile_lines(path: Path):
    """
    Read the dockerfile and return a list of lines with
    trailing newline + trailing whitespace stripped.
    """
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n").rstrip() for line in f]


# --------------------------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------------------------
def test_repository_directories_exist():
    """Top-level and service directories must exist."""
    assert APP_DIR.is_dir(), f"Expected directory {APP_DIR} to exist."
    assert SERVICE_A_DIR.is_dir(), f"Expected directory {SERVICE_A_DIR} to exist."
    assert SERVICE_B_DIR.is_dir(), f"Expected directory {SERVICE_B_DIR} to exist."


@pytest.mark.parametrize(
    "dockerfile_path",
    [SERVICE_A_DOCKERFILE, SERVICE_B_DOCKERFILE],
)
def test_dockerfiles_exist(dockerfile_path):
    """Dockerfile must exist in each service directory."""
    assert dockerfile_path.is_file(), f"Missing {dockerfile_path}"


def test_service_a_dockerfile_contents():
    """service-a/Dockerfile must match the expected three lines exactly."""
    lines = read_dockerfile_lines(SERVICE_A_DOCKERFILE)
    assert (
        lines == EXPECTED_CONTENT_SERVICE_A
    ), f"{SERVICE_A_DOCKERFILE} contents do not match expectations.\nExpected: {EXPECTED_CONTENT_SERVICE_A}\nActual:   {lines}"


def test_service_b_dockerfile_contents():
    """service-b/Dockerfile must match the expected three lines exactly."""
    lines = read_dockerfile_lines(SERVICE_B_DOCKERFILE)
    assert (
        lines == EXPECTED_CONTENT_SERVICE_B
    ), f"{SERVICE_B_DOCKERFILE} contents do not match expectations.\nExpected: {EXPECTED_CONTENT_SERVICE_B}\nActual:   {lines}"


def test_dockerfile_add_usage():
    """
    Sanity check: service-b must contain exactly one ADD instruction,
    service-a must contain none.
    """
    add_lines_a = [
        (idx + 1, line)
        for idx, line in enumerate(read_dockerfile_lines(SERVICE_A_DOCKERFILE))
        if "ADD" in line
    ]
    add_lines_b = [
        (idx + 1, line)
        for idx, line in enumerate(read_dockerfile_lines(SERVICE_B_DOCKERFILE))
        if "ADD" in line
    ]

    assert (
        not add_lines_a
    ), f"'ADD' instruction found in {SERVICE_A_DOCKERFILE}: {add_lines_a}"
    assert (
        add_lines_b == [(2, "ADD . /usr/src/app")]
    ), f"'ADD' instruction in {SERVICE_B_DOCKERFILE} is missing or incorrect. Found: {add_lines_b}"