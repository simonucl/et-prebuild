# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state before the student begins the assignment described in the prompt.
#
# The tests assert that:
#   • The raw input file /home/user/datasets/chat_samples.txt exists,
#     has the correct permissions, and its **exact** eight-line content
#     (including punctuation and trailing newlines) is intact.
#   • The two deliverable files that the student is expected to create
#     later—/home/user/datasets/chat_samples_freq.tsv and
#     /home/user/datasets/build_freq_commands.log—do **not** exist yet.
#
# The suite relies only on the Python standard library plus pytest.

import os
import stat
from pathlib import Path

import pytest

# Base paths used throughout the tests
HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"

RAW_FILE = DATASETS_DIR / "chat_samples.txt"
FREQ_FILE = DATASETS_DIR / "chat_samples_freq.tsv"
LOG_FILE = DATASETS_DIR / "build_freq_commands.log"

# Expected exact content of chat_samples.txt (including newlines)
EXPECTED_RAW_LINES = [
    "Hello world, hello AI!\n",
    "The AI world is vast.\n",
    "Machine learning fuels the AI revolution.\n",
    "Hello again, machine learning world.\n",
    "AI and machine learning are related fields.\n",
    "World of hello messages.\n",
    "AI says hello to the world.\n",
    "Learning about machine intelligence.\n",
]


def _file_mode(path: Path) -> int:
    """
    Return the permission bits (e.g. 0o644) for a given path.
    """
    return stat.S_IMODE(path.stat().st_mode)


@pytest.fixture(scope="module")
def raw_file_contents():
    """
    Read and return the raw file contents once per test session.
    """
    if not RAW_FILE.exists():
        pytest.skip(f"{RAW_FILE} does not exist; skipping content checks")
    return RAW_FILE.read_text(encoding="utf-8", errors="strict")


def test_datasets_directory_exists():
    assert DATASETS_DIR.is_dir(), (
        f"Required directory {DATASETS_DIR} is missing. "
        "It must exist before any processing begins."
    )


def test_raw_chat_file_exists_with_correct_permissions():
    assert RAW_FILE.is_file(), (
        f"Required raw data file {RAW_FILE} is missing. "
        "It must be present before the student starts."
    )

    expected_mode = 0o644
    actual_mode = _file_mode(RAW_FILE)
    assert actual_mode == expected_mode, (
        f"{RAW_FILE} should have permissions {oct(expected_mode)}, "
        f"but has {oct(actual_mode)} instead."
    )


def test_raw_chat_file_has_exact_expected_content(raw_file_contents):
    # Verify byte-for-byte content
    actual_lines = raw_file_contents.splitlines(keepends=True)

    assert actual_lines == EXPECTED_RAW_LINES, (
        "The content of /home/user/datasets/chat_samples.txt does not match the "
        "expected eight-line reference.  If this file was modified, restore it "
        "to the original state shown in the task description."
    )


@pytest.mark.parametrize("path", [FREQ_FILE, LOG_FILE])
def test_expected_output_files_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"{path} should NOT exist prior to running the student's solution. "
        "Found an unexpected file; please remove it before starting."
    )