# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state *before* the student
performs any actions for the "compress rotated log files" exercise.

The checks intentionally cover ONLY the pre-existing resources and never touch
(or even mention) the files that the student is expected to create later.
"""

from pathlib import Path
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "storage" / "logs"
ARCHIVES_DIR = HOME / "archives"

EXPECTED_LOG_FILES = [
    "app-2023-09-01.log",
    "app-2023-09-02.log",
    "app-2023-09-03.log",
]

EXPECTED_CONTENTS = {
    "app-2023-09-01.log": "Dummy log 1\n",
    "app-2023-09-02.log": "Dummy log 2\n",
    "app-2023-09-03.log": "Dummy log 3\n",
}


@pytest.fixture(scope="session")
def log_dir():
    return LOG_DIR


@pytest.fixture(scope="session")
def archives_dir():
    return ARCHIVES_DIR


def test_log_directory_exists(log_dir: Path):
    assert log_dir.exists(), (
        f"Expected the logs directory {log_dir} to exist, but it is missing."
    )
    assert log_dir.is_dir(), (
        f"Expected {log_dir} to be a directory, but it is not."
    )


def test_archives_directory_exists_and_is_empty(archives_dir: Path):
    assert archives_dir.exists(), (
        f"Expected the archives directory {archives_dir} to exist, but it is missing."
    )
    assert archives_dir.is_dir(), (
        f"Expected {archives_dir} to be a directory, but it is not."
    )
    contents = list(archives_dir.iterdir())
    assert not contents, (
        f"The archives directory {archives_dir} should be empty before the task "
        f"starts, but it contains: {[p.name for p in contents]}"
    )


def test_log_directory_contains_exact_files(log_dir: Path):
    actual_files = sorted(p.name for p in log_dir.iterdir() if p.is_file())
    expected_sorted = sorted(EXPECTED_LOG_FILES)
    assert actual_files == expected_sorted, (
        "The logs directory must contain exactly the three expected log files.\n"
        f"Expected: {expected_sorted}\n"
        f"Found:    {actual_files}"
    )


@pytest.mark.parametrize("filename", EXPECTED_LOG_FILES)
def test_each_log_file_exists_and_is_regular(log_dir: Path, filename: str):
    file_path = log_dir / filename
    assert file_path.exists(), f"Expected log file {file_path} to exist."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."


@pytest.mark.parametrize("filename,expected_content", EXPECTED_CONTENTS.items())
def test_log_file_contents(log_dir: Path, filename: str, expected_content: str):
    """
    The exact content strings are small and provided in the specification.
    Validating them helps catch accidental file truncation, wrong file ordering,
    or incorrect file placement.
    """
    file_path = log_dir / filename
    data = file_path.read_text(encoding="utf-8")
    assert data == expected_content, (
        f"Content mismatch in {file_path}.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(data)}"
    )