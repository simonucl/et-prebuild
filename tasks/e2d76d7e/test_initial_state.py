# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state **before**
# the student executes the archiving command.  These tests make sure the
# expected project files are in place and that no accidental changes have
# occurred.  They purposely do NOT touch or even mention the future output
# artefacts (the tarball or its manifest) — only the pre-existing state.

from pathlib import Path
import os
import stat
import pytest

HOME = Path("/home/user")

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def assert_read_text(path: Path, expected: str) -> None:
    """Read a UTF-8 file and compare its full text to *expected*."""
    assert path.is_file(), f"Expected file {path} does not exist."
    data = path.read_text(encoding="utf-8")
    assert data == expected, (
        f"Unexpected contents in {path}.\n"
        f"Expected ({len(expected)} bytes):\n{expected!r}\n"
        f"Got ({len(data)} bytes):\n{data!r}"
    )


# --------------------------------------------------------------------------- #
# Directory structure tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "directory",
    [
        HOME / "api-test",
        HOME / "api-test" / "config",
        HOME / "api-test" / "logs",
        HOME / "backup",
    ],
)
def test_directories_exist(directory: Path) -> None:
    assert directory.is_dir(), f"Required directory {directory} is missing."


def test_backup_dir_is_writable() -> None:
    """The backup directory must already be both present and writable."""
    backup_dir = HOME / "backup"
    # Directory existence is checked in test_directories_exist.
    is_writable = os.access(backup_dir, os.W_OK)
    assert is_writable, f"Directory {backup_dir} is not writable."


# --------------------------------------------------------------------------- #
# File existence tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "filepath",
    [
        HOME / "api-test" / "README.md",
        HOME / "api-test" / "config" / "config.yaml",
        HOME / "api-test" / "logs" / "2023-09-15_01.json",
        HOME / "api-test" / "logs" / "2023-09-16_01.json",
        HOME / "api-test" / "logs" / "2023-09-17_01.json",
    ],
)
def test_files_exist(filepath: Path) -> None:
    assert filepath.is_file(), f"Required file {filepath} is missing."


# --------------------------------------------------------------------------- #
# Exact content checks
# --------------------------------------------------------------------------- #
def test_readme_contents() -> None:
    readme = HOME / "api-test" / "README.md"
    expected = "API Test Project\n"
    assert_read_text(readme, expected)


def test_config_yaml_contents() -> None:
    cfg = HOME / "api-test" / "config" / "config.yaml"
    expected = (
        'endpoint: "https://example.com/api"\n'
        "retries: 3\n"
    )
    assert_read_text(cfg, expected)


@pytest.mark.parametrize(
    "file_name,expected_date",
    [
        ("2023-09-15_01.json", "2023-09-15"),
        ("2023-09-16_01.json", "2023-09-16"),
        ("2023-09-17_01.json", "2023-09-17"),
    ],
)
def test_log_file_contents(file_name: str, expected_date: str) -> None:
    log_file = HOME / "api-test" / "logs" / file_name
    expected = f'{{"status":"ok","date":"{expected_date}"}}\n'
    assert_read_text(log_file, expected)


# --------------------------------------------------------------------------- #
# Directory should contain only the expected log files (no surprises).
# --------------------------------------------------------------------------- #
def test_logs_directory_has_expected_files_only() -> None:
    logs_dir = HOME / "api-test" / "logs"
    expected_files = {
        "2023-09-15_01.json",
        "2023-09-16_01.json",
        "2023-09-17_01.json",
    }
    actual_files = {p.name for p in logs_dir.iterdir() if p.is_file()}
    assert actual_files == expected_files, (
        f"Unexpected contents in {logs_dir}.\n"
        f"Expected exactly: {sorted(expected_files)}\n"
        f"Found: {sorted(actual_files)}"
    )