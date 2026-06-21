# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / file-system
state *before* the student begins the task.

What we check:
1. The reference directory /home/user/reference exists and is a directory.
2. The reference data file /home/user/reference/perf_sample.dat exists,
   is a regular file, is readable, and contains exactly the expected data.
3. The reference file contains the three required KEY=VALUE pairs with
   the exact values specified by the task description.

We explicitly do NOT test for any output directories or files that the
student is supposed to create later (e.g. /home/user/compliance_audit/*).
"""

import os
import stat
import pytest

REFERENCE_DIR = "/home/user/reference"
REFERENCE_FILE = "/home/user/reference/perf_sample.dat"

# The expected, authoritative content of the reference data file.
EXPECTED_CONTENT = (
    "CPU_MAX_OPS=7845\n"
    "DISK_AVG_LAT_MS=3.45\n"
    "MEM_AVAIL_MB=2034\n"
)


def test_reference_directory_exists():
    """The /home/user/reference directory must exist and be a directory."""
    assert os.path.exists(REFERENCE_DIR), (
        f"Required directory {REFERENCE_DIR} does not exist. "
        "The task cannot proceed without it."
    )
    assert os.path.isdir(REFERENCE_DIR), (
        f"{REFERENCE_DIR} exists but is not a directory."
    )


def test_reference_file_exists_and_is_regular():
    """The reference data file must exist, be a regular file, and be readable."""
    assert os.path.exists(REFERENCE_FILE), (
        f"Required file {REFERENCE_FILE} does not exist."
    )
    st = os.stat(REFERENCE_FILE)
    assert stat.S_ISREG(st.st_mode), (
        f"{REFERENCE_FILE} exists but is not a regular file."
    )
    # Attempt to open the file to ensure it is readable.
    try:
        with open(REFERENCE_FILE, "r", encoding="utf-8") as fh:
            fh.read(1)
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Cannot read {REFERENCE_FILE}: {exc}")


def test_reference_file_content_exact_match():
    """
    The reference file must contain exactly the expected content,
    including line order and the trailing newline.
    """
    with open(REFERENCE_FILE, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert actual_content == EXPECTED_CONTENT, (
        f"Contents of {REFERENCE_FILE} do not match the expected data.\n\n"
        "Expected (repr):\n"
        f"{repr(EXPECTED_CONTENT)}\n\n"
        "Actual (repr):\n"
        f"{repr(actual_content)}"
    )