# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / file-system
# state before the student begins any work.  It confirms that the toy
# project is present and that none of the “deliverables” (archive, PID
# file, releases/, or logs/) have been created yet.

import os
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project")
README = PROJECT_ROOT / "README.md"
SRC_DIR = PROJECT_ROOT / "src"
MAIN_PY = SRC_DIR / "main.py"

ARCHIVE_PID = Path("/home/user/archive.pid")
RELEASES_DIR = Path("/home/user/releases")
ARCHIVE_FILE = RELEASES_DIR / "release-v1.tar.gz"
LOGS_DIR = Path("/home/user/logs")
LOG_FILE = LOGS_DIR / "release.log"


def test_project_directory_structure_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Expected project directory {PROJECT_ROOT} to exist."
    )
    assert README.is_file(), (
        f"Expected README file {README} to exist."
    )
    assert SRC_DIR.is_dir(), (
        f"Expected source directory {SRC_DIR} to exist."
    )
    assert MAIN_PY.is_file(), (
        f"Expected main source file {MAIN_PY} to exist."
    )


def test_readme_contents():
    expected = "Demo project for packaging\n"
    content = README.read_text()
    assert content == expected, (
        f"README.md content mismatch.\n"
        f"Expected exactly: {expected!r}\n"
        f"Got: {content!r}"
    )


def test_main_py_contents():
    expected = 'print("Hello, packaged world!")\n'
    content = MAIN_PY.read_text()
    assert content == expected, (
        f"src/main.py content mismatch.\n"
        f"Expected exactly: {expected!r}\n"
        f"Got: {content!r}"
    )


def test_no_release_artifacts_yet():
    # None of the output artefacts should exist before the student starts.
    assert not ARCHIVE_PID.exists(), (
        f"Found unexpected PID file: {ARCHIVE_PID}. "
        "It should not exist before running the workflow."
    )
    assert not RELEASES_DIR.exists(), (
        f"Found unexpected releases directory: {RELEASES_DIR}. "
        "It should not exist before running the workflow."
    )
    assert not ARCHIVE_FILE.exists(), (
        f"Found unexpected archive file: {ARCHIVE_FILE}. "
        "It should not exist before running the workflow."
    )
    assert not LOG_FILE.exists(), (
        f"Found unexpected log file: {LOG_FILE}. "
        "It should not exist before running the workflow."
    )