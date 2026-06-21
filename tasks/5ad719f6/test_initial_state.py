# test_initial_state.py
#
# This test-suite verifies that the workstation is in the *initial* state
# expected *before* the student starts writing any code.
#
# 1. Mandatory inputs must already exist and contain the exact reference data.
# 2. No output artefacts from a previous run may be present.
#
# If any assertion fails the error message will *precisely* tell the student
# what is wrong or missing so they can fix the environment before continuing.
#
# Only the Python standard-library plus pytest are used, as required.

import os
import stat
from pathlib import Path
import configparser
import pytest

# ---------------------------------------------------------------------------
# Fixed absolute paths (do *not* change)
RAW_CSV_PATH      = Path("/home/user/data/raw/customers.csv")
INI_PATH          = Path("/home/user/config/cleaning.ini")
PROCESSED_DIR     = Path("/home/user/data/processed")
CLEANED_CSV_PATH  = PROCESSED_DIR / "customers_cleaned.csv"
LOG_DIR           = Path("/home/user/logs")
LOG_PATH          = LOG_DIR / "cleaning.log"

# ---------------------------------------------------------------------------
# Helper: expected reference data (LF line-endings only)

EXPECTED_RAW_CSV = (
    "customer_id,full_name,email,age,country,phone\n"
    "1,John Doe,jdoe@example.com,29,USA,555-1234\n"
    "2,Jane Smith,,34,Canada,555-2345\n"
    "3,,third@example.com,27,USA,\n"
    "4,Bob Lee,blee@example.com,,USA,555-4567\n"
    "5,Alice Wong,awong@example.com,31,,555-5678\n"
)

EXPECTED_INI_VALUES = {
    "keep": {
        "list": "customer_id,full_name,email,age,country",
    },
    "rename": {
        "customer_id": "id",
        "full_name":   "name",
        "email":       "email_address",
    },
    "drop": {
        "policy": "any",
    },
}

# ---------------------------------------------------------------------------
# Tests

def test_raw_csv_exists_and_is_correct():
    """The raw customer CSV must exist and match the exact reference data."""
    assert RAW_CSV_PATH.exists(), (
        f"Missing required input file: {RAW_CSV_PATH}"
    )

    # The file must be a regular file (not a dir, symlink, etc.).
    assert RAW_CSV_PATH.is_file(), (
        f"Expected a regular file at {RAW_CSV_PATH}, but found something else."
    )

    # Permission check: readable by the current (non-root) user.
    assert os.access(RAW_CSV_PATH, os.R_OK), (
        f"File {RAW_CSV_PATH} exists but is not readable."
    )

    # Read and compare exact text (including final newline).
    actual = RAW_CSV_PATH.read_text(encoding="utf-8")
    assert actual == EXPECTED_RAW_CSV, (
        f"Content mismatch in {RAW_CSV_PATH}.\n"
        f"--- Expected (first 120 chars) ---\n{EXPECTED_RAW_CSV[:120]!r}\n"
        f"--- Actual   (first 120 chars) ---\n{actual[:120]!r}"
    )


def test_ini_file_exists_and_has_expected_values():
    """The INI configuration must exist and contain the reference settings."""
    assert INI_PATH.exists(), f"Missing required INI file: {INI_PATH}"
    assert INI_PATH.is_file(), f"Expected a regular file at {INI_PATH}."

    config = configparser.ConfigParser(interpolation=None)
    # Preserve case & spacing exactly as in the file for robust comparison.
    with INI_PATH.open("r", encoding="utf-8") as fp:
        config.read_file(fp)

    # 1) Section names -------------------------------------------------------
    expected_sections = set(EXPECTED_INI_VALUES.keys())
    actual_sections   = set(config.sections())
    assert actual_sections == expected_sections, (
        "INI sections mismatch.\n"
        f"Expected sections: {sorted(expected_sections)}\n"
        f"Actual sections:   {sorted(actual_sections)}"
    )

    # 2) Each key/value pair -------------------------------------------------
    for section, keyvals in EXPECTED_INI_VALUES.items():
        for key, expected_val in keyvals.items():
            assert config.has_option(section, key), (
                f"INI file is missing key '{key}' in section [{section}]."
            )
            actual_val = config.get(section, key, raw=True)
            assert actual_val == expected_val, (
                f"INI mismatch in section [{section}], key '{key}'.\n"
                f"Expected value: {expected_val!r}\n"
                f"Actual value:   {actual_val!r}"
            )


def test_no_processed_outputs_exist_yet():
    """
    Before the student runs their script, no processed artefacts should exist.
    This prevents stale data from causing false positives during grading.
    """
    if PROCESSED_DIR.exists():
        # The directory itself is allowed to exist but must be empty.
        dir_contents = list(PROCESSED_DIR.iterdir())
        assert CLEANED_CSV_PATH not in dir_contents, (
            f"Output file {CLEANED_CSV_PATH} already exists. "
            "Remove it before running your cleaning script."
        )
        # Optionally insist the directory is empty to be extra strict.
        assert not dir_contents, (
            f"Directory {PROCESSED_DIR} should be empty initially.\n"
            f"Current contents: {[str(p) for p in dir_contents]}"
        )

    # The cleaned CSV must definitely *not* exist.
    assert not CLEANED_CSV_PATH.exists(), (
        f"Output file {CLEANED_CSV_PATH} is present but should not exist yet."
    )

    # Similarly, the log directory must not already contain the cleaning log.
    if LOG_DIR.exists():
        assert not LOG_PATH.exists(), (
            f"Log file {LOG_PATH} already exists. "
            "Please remove it before starting the task."
        )