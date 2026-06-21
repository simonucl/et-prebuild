# test_initial_state.py
#
# Pytest suite that verifies the OS / filesystem *before* the student
# performs any actions for the “capacity-planning” exercise.
#
# It checks that the raw input statistics are present and contain
# exactly the expected contents.  Nothing related to the expected
# output (/home/user/reports/…) is validated here, per the grading
# requirements.

from pathlib import Path
import pytest

RAW_DIR = Path("/home/user/raw_stats")
EXPECTED_FILES = {
    "containerA.txt": (
        "CPU: 17.5\n"
        "Memory_Used_MB: 256\n"
        "Memory_Limit_MB: 1024\n"
        "Network_In_KB: 10240\n"
        "Network_Out_KB: 20480\n"
    ),
    "containerB.txt": (
        "CPU: 42.3\n"
        "Memory_Used_MB: 512\n"
        "Memory_Limit_MB: 2048\n"
        "Network_In_KB: 5120\n"
        "Network_Out_KB: 10240\n"
    ),
}


def test_raw_stats_directory_exists():
    """
    /home/user/raw_stats/ must already exist and be a directory before the
    student starts processing data.
    """
    assert RAW_DIR.exists(), f"Required directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename", EXPECTED_FILES.keys())
def test_required_files_present(filename):
    """
    Every expected raw statistics file must be present in /home/user/raw_stats/.
    """
    file_path = RAW_DIR / filename
    assert file_path.exists(), f"Missing required input file: {file_path}"
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_file_contents_exact(filename, expected_content):
    """
    The contents of each raw statistics file must match the exercise
    specification exactly (byte-for-byte), including final newlines.
    """
    file_path = RAW_DIR / filename
    actual_content = file_path.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), (
        f"Contents of {file_path} do not match the expected template.\n"
        "---- Expected ----\n"
        f"{expected_content!r}\n"
        "----   Got   ----\n"
        f"{actual_content!r}"
    )