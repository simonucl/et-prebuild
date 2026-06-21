# test_initial_state.py
#
# This pytest suite validates the operating-system / filesystem **before**
# the student performs any action.  It ensures that the starter data exists
# exactly as expected and that no output artefacts have been created yet.

import os
import textwrap
from pathlib import Path

DATA_DIR = Path("/home/user/data")
RAW_FILE = DATA_DIR / "raw_measurements.csv"

SUMMARY_STATS = DATA_DIR / "summary_stats.txt"
RAW_SPACE = DATA_DIR / "raw_measurements_space.txt"
TEMP_ONLY = DATA_DIR / "temperature_only.tsv"
PROCESS_LOG = DATA_DIR / "process.log"

EXPECTED_RAW_CONTENT = textwrap.dedent("""\
    subject_id,temperature,heart_rate
    S1,36.6,72
    S2,37.1,75
    S3,36.9,70
    S4,37.3,80
    S5,36.8,68
    """)  # Note: textwrap removes leading indentation only.


def test_data_directory_exists():
    """The /home/user/data directory must exist."""
    assert DATA_DIR.is_dir(), f"Required directory {DATA_DIR} is missing."


def test_raw_measurements_exists_with_correct_content():
    """
    Validate that the raw CSV file exists and its content matches the spec,
    including the final trailing newline.
    """
    assert RAW_FILE.is_file(), f"Required file {RAW_FILE} is missing."

    # Read in *binary* mode to avoid newline translation surprises.
    content_bytes = RAW_FILE.read_bytes()
    try:
        content_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        assert False, f"{RAW_FILE} is not valid UTF-8: {exc}"

    # Ensure the file ends with exactly one newline character.
    assert content_text.endswith(
        "\n"
    ), f"{RAW_FILE} must terminate with a single newline (\\n)."

    # Compare full content.
    expected = EXPECTED_RAW_CONTENT
    assert (
        content_text == expected
    ), (
        f"Content of {RAW_FILE} does not match the expected starter data.\n"
        "Expected:\n"
        "------------------\n"
        f"{expected}"
        "------------------\n"
        "Found:\n"
        "------------------\n"
        f"{content_text}"
        "------------------"
    )


def test_no_output_files_yet():
    """
    None of the derived artefacts should exist before the student runs
    their solution.
    """
    for path in (SUMMARY_STATS, RAW_SPACE, TEMP_ONLY, PROCESS_LOG):
        assert (
            not path.exists()
        ), f"File {path} should NOT exist yet, but it does."