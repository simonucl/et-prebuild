# test_initial_state.py
#
# This test-suite validates the state of the filesystem *before* the student
# executes any command.  It asserts that the expected project layout, file
# contents and pre-existing directories are exactly as described in the task
# specification.  If any assertion fails the error message will clearly
# indicate what is missing or differs from the required initial state.
#
# NOTE:
# • We intentionally do NOT test for the presence of the output file
#   (/home/user/scan/latest_tag_findings.log) because it will be created by
#   the student’s solution.
# • We use only the Python standard library and pytest.

import os
from pathlib import Path

PROJECT_ROOT = Path("/home/user/microservices").resolve()
SCAN_DIR = Path("/home/user/scan").resolve()

EXPECTED_FILES = {
    PROJECT_ROOT / "service-a" / "Dockerfile": [
        "FROM python:3.9-slim",
        "# Simple API service",
    ],
    PROJECT_ROOT / "service-b" / "Dockerfile": [
        "FROM ubuntu:latest",
        "RUN apt-get update && apt-get install -y curl",
    ],
    PROJECT_ROOT / "service-c" / "Dockerfile": [
        "FROM node:14",
        "WORKDIR /usr/src/app",
    ],
}


def _read_file_lines(path: Path):
    """Return the file's lines without the trailing newline character."""
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()]


def test_project_root_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Expected project root directory {PROJECT_ROOT} to exist and be a directory."
    )


def test_expected_dockerfiles_exist_and_have_correct_content():
    """
    Ensure each expected Dockerfile exists with exactly the declared lines.
    The comparison is strict—spacing, casing, and line order must match.
    """
    for path, expected_lines in EXPECTED_FILES.items():
        assert path.is_file(), f"Missing file: {path}"
        actual_lines = _read_file_lines(path)
        assert (
            actual_lines == expected_lines
        ), (
            f"Content mismatch in {path}.\n"
            f"Expected lines:\n{expected_lines}\n"
            f"Actual lines:\n{actual_lines}"
        )


def test_no_extra_dockerfiles_present():
    """
    There should be exactly three Dockerfiles—one per service as listed in
    EXPECTED_FILES.  This guards against stray files that might influence the
    student's search command.
    """
    dockerfiles_found = list(PROJECT_ROOT.rglob("Dockerfile"))
    expected_set = set(EXPECTED_FILES.keys())
    found_set = set(dockerfiles_found)

    # Check for unexpected files
    unexpected = found_set - expected_set
    assert not unexpected, (
        f"Unexpected Dockerfile(s) present: {sorted(map(str, unexpected))}"
    )

    # Check for missing files (redundant with earlier test but yields clearer diff)
    missing = expected_set - found_set
    assert not missing, f"Expected Dockerfile(s) not found: {sorted(map(str, missing))}"


def test_scan_directory_exists_and_is_empty():
    """
    The directory /home/user/scan must exist, be writable, and be empty
    (no files) before the student runs their command.
    """
    assert SCAN_DIR.is_dir(), f"Expected scan directory {SCAN_DIR} to exist."
    # Check writability
    temp_test_path = SCAN_DIR / ".pytest_write_test"
    try:
        with temp_test_path.open("w") as tmp:
            tmp.write("ok")
    finally:
        if temp_test_path.exists():
            temp_test_path.unlink()

    # Ensure directory is empty after cleanup
    remaining_contents = [p.name for p in SCAN_DIR.iterdir() if p.exists()]
    assert (
        not remaining_contents
    ), f"{SCAN_DIR} should be empty, but contains: {remaining_contents}"