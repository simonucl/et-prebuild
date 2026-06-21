# test_initial_state.py
#
# Pytest suite that validates the initial, pre-task state of the
# operating system / filesystem for the “cluster telemetry trimming”
# exercise.  These tests make sure the required input data is present
# and that no output artefacts exist yet, so that subsequent grading
# can rely on a clean, known-good starting point.

import os
import stat
import pytest

# ---------- CONSTANTS ----------
INPUT_FILE = "/home/user/data/cluster_resource_usage.tsv"
OUTPUT_DIR = "/home/user/output"
CSV_FILE   = os.path.join(OUTPUT_DIR, "usage_trimmed.csv")
LOG_FILE   = os.path.join(OUTPUT_DIR, "usage_trimmed.log")

EXPECTED_TSV_CONTENT = (
    "Timestamp\tNode\tCPU_Used\tCPU_Total\tMemory_Used\tMemory_Total\tDisk_Used\tDisk_Total\n"
    "2023-08-07T00:00:00Z\tnode01\t45\t64\t32768\t65536\t120\t250\n"
    "2023-08-07T00:00:00Z\tnode02\t53\t64\t41984\t65536\t140\t250\n"
    "2023-08-07T01:00:00Z\tnode01\t47\t64\t33000\t65536\t121\t250\n"
    "2023-08-07T01:00:00Z\tnode02\t52\t64\t42050\t65536\t141\t250\n"
    "2023-08-07T02:00:00Z\tnode01\t49\t64\t33100\t65536\t122\t250\n"
)

# ---------- TESTS ----------
def test_input_file_exists_and_is_regular_file():
    """The raw telemetry file must exist and be a regular, readable file."""
    assert os.path.isfile(INPUT_FILE), (
        f"Required input file not found: {INPUT_FILE}"
    )
    mode = os.stat(INPUT_FILE).st_mode
    assert stat.S_ISREG(mode), (
        f"{INPUT_FILE} exists but is not a regular file."
    )
    # Readability check: current user (pytest) must be able to open it.
    try:
        with open(INPUT_FILE, "rb"):
            pass
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not open {INPUT_FILE} for reading: {exc}")

def test_input_file_has_exact_expected_content():
    """Verify the TSV file matches the byte-for-byte canonical content."""
    with open(INPUT_FILE, "r", encoding="utf-8", newline="") as fh:
        content = fh.read()

    # Accept either presence or absence of a trailing newline.
    possibilities = {
        EXPECTED_TSV_CONTENT,
        EXPECTED_TSV_CONTENT.rstrip("\n"),
    }

    assert content in possibilities, (
        "The content of the input TSV file does not match the expected "
        "canonical data.\n\n"
        "Expected (\\t represents TAB):\n"
        f"{EXPECTED_TSV_CONTENT!r}\n\n"
        "Actual:\n"
        f"{content!r}"
    )

    # Sanity-check line count.
    line_count = len(content.splitlines())
    assert line_count == 6, (
        f"Input TSV should have exactly 6 lines (1 header + 5 data), "
        f"but has {line_count}."
    )

def test_output_directory_and_files_do_not_exist_yet():
    """
    Prior to running the student’s command, the /home/user/output directory
    (and any expected files within it) must NOT exist so that the task
    can create them from scratch.
    """
    assert not os.path.exists(OUTPUT_DIR), (
        f"Output directory {OUTPUT_DIR} already exists; initial state should "
        "be clean."
    )
    assert not os.path.exists(CSV_FILE), (
        f"Unexpected CSV file found at {CSV_FILE} before the task has run."
    )
    assert not os.path.exists(LOG_FILE), (
        f"Unexpected log file found at {LOG_FILE} before the task has run."
    )