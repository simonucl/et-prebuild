# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must be
# present *before* the student executes any commands.  If any of these tests
# fail, the exercise cannot be started because the baseline environment is
# already incorrect.

import os
from pathlib import Path
import pytest

# Base directories
HOME = Path("/home/user")
PROJECTS = HOME / "projects"
MICRO_DIR = PROJECTS / "microservices"
BACKUP_DIR = PROJECTS / "config_backup"

# Expected configuration files and their canonical contents
EXPECTED_CONFIG_FILES = {
    MICRO_DIR / "serviceA" / "deploy.yaml":
        "version: 'A'\n",
    MICRO_DIR / "serviceA" / ".env":
        "SERVICE=serviceA\nDB=mysql\n",
    MICRO_DIR / "serviceB" / "app.yaml":
        "service: B\nreplicas: 3\n",
    MICRO_DIR / "serviceB" / ".env":
        "SERVICE=serviceB\nDB=postgres\n",
    MICRO_DIR / "serviceC" / "infra.yaml":
        "infra: true\nregion: us-east-1\n",
    MICRO_DIR / "serviceC" / ".env":
        "SERVICE=serviceC\nDB=mongodb\n",
}

# A non-config file we also expect to exist (to ensure the copy
# requirement filters it out later on).
NON_CONFIG_FILE = MICRO_DIR / "serviceA" / "readme.txt"
NON_CONFIG_CONTENT = "Service A documentation\n"


def test_microservices_directory_exists_and_is_directory():
    assert MICRO_DIR.exists(), f"Required directory {MICRO_DIR} is missing."
    assert MICRO_DIR.is_dir(), f"{MICRO_DIR} exists but is not a directory."


def test_config_backup_directory_absent_initially():
    assert not BACKUP_DIR.exists(), (
        f"Directory {BACKUP_DIR} should NOT exist before the student runs their "
        "solution, but it is already present."
    )


@pytest.mark.parametrize("path,expected_content", EXPECTED_CONFIG_FILES.items())
def test_expected_config_files_exist_with_correct_content(path: Path, expected_content: str):
    assert path.exists(), f"Required configuration file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    # Verify file contents exactly, byte-for-byte.
    actual_content = path.read_text()
    assert actual_content == expected_content, (
        f"File {path} has unexpected content.\n"
        f"Expected:\n{expected_content!r}\nActual:\n{actual_content!r}"
    )


def test_only_expected_config_files_present_initially():
    """
    Ensure that the only *.yaml and *.env files present under the microservices
    tree are exactly those enumerated in EXPECTED_CONFIG_FILES.  This guarantees
    that the grader's later count (exactly six) is meaningful.
    """
    found = {
        p
        for p in MICRO_DIR.rglob("*")
        if p.is_file() and p.name.endswith((".yaml", ".env"))
    }
    assert found == set(EXPECTED_CONFIG_FILES.keys()), (
        "The set of *.yaml and *.env files under the microservices directory "
        "does not match the expected baseline.\n"
        f"Expected ({len(EXPECTED_CONFIG_FILES)}):\n"
        + "\n".join(sorted(map(str, EXPECTED_CONFIG_FILES.keys())))
        + "\n\nFound ({len(found)}):\n"
        + "\n".join(sorted(map(str, found)))
    )


def test_non_config_file_exists_and_has_expected_content():
    assert NON_CONFIG_FILE.exists(), f"Expected file {NON_CONFIG_FILE} is missing."
    assert NON_CONFIG_FILE.is_file(), f"{NON_CONFIG_FILE} exists but is not a regular file."
    actual = NON_CONFIG_FILE.read_text()
    assert actual == NON_CONFIG_CONTENT, (
        f"File {NON_CONFIG_FILE} has unexpected content.\n"
        f"Expected:\n{NON_CONFIG_CONTENT!r}\nActual:\n{actual!r}"
    )