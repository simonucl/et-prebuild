# test_initial_state.py
#
# Pytest suite to validate the *initial* filesystem / OS state
# BEFORE the student performs any processing.
#
# What we check:
#   1. The raw data file /home/user/data/sales_q1.csv must exist
#      and contain exactly the expected eight lines (1 header + 7 data rows).
#   2. The output directory /home/user/output must NOT yet contain any of the
#      artefacts that the student is supposed to create
#      (top_products.json, summary.csv, process.log).
#      It is acceptable for the directory to be absent or to exist but be empty.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path
import pytest

RAW_FILE = Path("/home/user/data/sales_q1.csv")
OUTPUT_DIR = Path("/home/user/output")
OUTPUT_FILES = {
    "top_products": OUTPUT_DIR / "top_products.json",
    "summary": OUTPUT_DIR / "summary.csv",
    "log": OUTPUT_DIR / "process.log",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_text(path: Path) -> str:
    """Read a text file using UTF-8 and raise a useful error if it fails."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Expected file {path} to exist, but it is missing.")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_raw_file_exists_and_contents_ok():
    """Verify the raw CSV exists and its contents are exactly as advertised."""
    assert RAW_FILE.is_file(), (
        f"Required raw data file {RAW_FILE} is missing. "
        "It must be present before the student starts."
    )

    expected_lines = [
        "Date,Region,Product,Quantity,Unit_Price",
        "2023-01-03,North,Widget,30,9.99",
        "2023-01-05,South,Gadget,20,14.95",
        "2023-02-10,East,Widget,45,9.99",
        "2023-02-14,West,Doohickey,50,4.50",
        "2023-03-01,North,Gadget,25,14.95",
        "2023-03-12,South,Widget,75,9.99",
        "2023-03-20,East,Doohickey,40,4.50",
    ]

    file_text = read_text(RAW_FILE)
    # Splitlines keeps it newline-agnostic and drops the final empty line (if any)
    actual_lines = file_text.splitlines()
    assert (
        actual_lines == expected_lines
    ), "The contents of the raw CSV file do not match the expected initial data."


def test_output_directory_not_prepopulated():
    """
    The student must create /home/user/output and populate it; it should NOT
    already contain the final artefacts. The directory itself may or may not
    exist yet, but the specific files must be absent.
    """
    if OUTPUT_DIR.exists():
        assert OUTPUT_DIR.is_dir(), (
            f"{OUTPUT_DIR} exists but is not a directory."
        )
        # Directory exists – ensure it is empty
        existing_entries = list(OUTPUT_DIR.iterdir())
        # Filter out any hidden files (e.g., .gitkeep) to allow a clean repo setup
        visible_entries = [
            p.name for p in existing_entries if not p.name.startswith(".")
        ]
        assert (
            len(visible_entries) == 0
        ), (
            f"{OUTPUT_DIR} should be empty at the start, but it currently "
            f"contains: {', '.join(visible_entries)}"
        )
    else:
        # Directory does not yet exist – perfect.
        assert not any(
            p.exists() for p in OUTPUT_FILES.values()
        ), "Some output artefacts exist even though the output directory is missing."

    # Double-check individual files are absent regardless of dir state
    for key, path in OUTPUT_FILES.items():
        assert not path.exists(), (
            f"{path} already exists at the initial stage, but it should "
            "only be created by the student's solution."
        )