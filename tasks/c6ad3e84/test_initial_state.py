# test_initial_state.py
#
# Verify the *initial* filesystem state before the student performs any action.
# These tests will fail if:
#   • required raw data or directories are missing,
#   • unexpected files (e.g., the script or processed outputs) already exist,
#   • raw CSV contents do not exactly match the specification.
#
# Only Python’s standard library and pytest are used.

import os
from pathlib import Path

RAW_DIR = Path("/home/user/data/raw")
SCRIPTS_DIR = Path("/home/user/scripts")
LOGS_DIR = Path("/home/user/logs")
PROCESSED_DIR = Path("/home/user/data/processed")
SCRIPT_FILE = SCRIPTS_DIR / "prepare_dataset.sh"
RAW_PART1 = RAW_DIR / "raw_part1.csv"
RAW_PART2 = RAW_DIR / "raw_part2.csv"
PROCESSED_CSV = PROCESSED_DIR / "training_data.csv"
LOG_FILE = LOGS_DIR / "prepare_dataset.log"

EXPECTED_PART1 = (
    "id,text,label\n"
    "1,\"hello world\",greeting\n"
    "2,\"how are you\",question\n"
    "3,\"goodbye\",farewell\n"
)
EXPECTED_PART2 = (
    "id,text,label\n"
    "4,\"yes\",affirmation\n"
    "5,\"no\",negation\n"
)

def test_required_directories_exist():
    """Raw, scripts, and logs directories must exist before any processing."""
    for d in (RAW_DIR, SCRIPTS_DIR, LOGS_DIR):
        assert d.exists() and d.is_dir(), f"Required directory {d} is missing."

def test_scripts_and_logs_are_empty():
    """
    Before the student starts, /home/user/scripts and /home/user/logs
    must be empty directories.
    """
    for d in (SCRIPTS_DIR, LOGS_DIR):
        contents = [p for p in d.iterdir() if not p.name.startswith(".")]
        assert contents == [], f"Directory {d} should be empty initially but contains: {contents}"

def test_raw_files_exist_with_correct_content():
    """Both raw CSV fragments must exist and contain exactly the expected text."""
    for file_path, expected in ((RAW_PART1, EXPECTED_PART1), (RAW_PART2, EXPECTED_PART2)):
        assert file_path.exists() and file_path.is_file(), f"Missing required file: {file_path}"
        data = file_path.read_text(encoding="utf-8")
        assert data == expected, (
            f"Content of {file_path} does not match specification.\n"
            "Expected:\n"
            "---------\n"
            f"{expected}\n"
            "Found:\n"
            "------\n"
            f"{data}"
        )

def test_processed_assets_do_not_yet_exist():
    """
    The processed directory, processed CSV, log file, and script must *not* exist
    at the initial checkpoint.
    """
    assert not PROCESSED_DIR.exists(), (
        f"{PROCESSED_DIR} should not exist yet; it must be created by the script."
    )
    for unexpected in (PROCESSED_CSV, LOG_FILE, SCRIPT_FILE):
        assert not unexpected.exists(), f"Unexpected pre-existing file: {unexpected}"