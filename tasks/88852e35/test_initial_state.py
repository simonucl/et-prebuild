# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem / OS state
# before the student performs any work.  Only the raw API dump is
# expected to exist; no derived artefacts or output directories/files
# should be present yet.

import os
from pathlib import Path

RAW_JSON_PATH = Path("/home/user/project/raw/api_responses.json")

# Exact content (including leading/trailing whitespace and the final LF newline)
EXPECTED_RAW_CONTENT = (
    "[\n"
    "  {\"id\":1,\"user\":\"alice\",\"amount\":120.50,\"status\":\"completed\",\"timestamp\":\"2023-01-15T10:25:00Z\"},\n"
    "  {\"id\":2,\"user\":\"bob\",\"amount\":200.00,\"status\":\"refunded\",\"timestamp\":\"2023-02-20T13:40:00Z\"},\n"
    "  {\"id\":3,\"user\":\"carol\",\"amount\":75.25,\"status\":\"completed\",\"timestamp\":\"2022-11-05T09:10:00Z\"},\n"
    "  {\"id\":4,\"user\":\"dave\",\"amount\":300.10,\"status\":\"completed\",\"timestamp\":\"2023-03-12T16:55:00Z\"},\n"
    "  {\"id\":5,\"user\":\"erin\",\"amount\":50.00,\"status\":\"pending\",\"timestamp\":\"2023-03-30T08:30:00Z\"},\n"
    "  {\"id\":6,\"user\":\"frank\",\"amount\":180.75,\"status\":\"completed\",\"timestamp\":\"2022-12-22T19:00:00Z\"},\n"
    "  {\"id\":7,\"user\":\"grace\",\"amount\":215.40,\"status\":\"completed\",\"timestamp\":\"2023-04-18T11:45:00Z\"},\n"
    "  {\"id\":8,\"user\":\"heidi\",\"amount\":90.00,\"status\":\"refunded\",\"timestamp\":\"2023-04-20T12:15:00Z\"}\n"
    "]\n"
)

DATA_DIR = Path("/home/user/project/data")
SCRIPTS_DIR = Path("/home/user/project/scripts")

CSV_PATH = DATA_DIR / "transactions_2023.csv"
SUMMARY_JSON_PATH = DATA_DIR / "summary.json"
LOG_PATH = SCRIPTS_DIR / "process.log"


def test_raw_api_dump_exists_with_exact_content():
    """Verify that the pre-existing raw JSON file is present and correct."""
    assert RAW_JSON_PATH.is_file(), (
        f"Required file not found: {RAW_JSON_PATH}"
    )

    # Read as binary to check line endings first
    raw_bytes = RAW_JSON_PATH.read_bytes()
    assert b"\r" not in raw_bytes, (
        f"File {RAW_JSON_PATH} must use Unix (LF) line endings only; "
        "carriage returns (CR) were found."
    )

    # UTF-8 decode check
    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError(
            f"File {RAW_JSON_PATH} is not valid UTF-8: {exc}"
        ) from exc

    assert raw_text == EXPECTED_RAW_CONTENT, (
        f"Content of {RAW_JSON_PATH} differs from the expected initial dump.\n"
        "If you intentionally modified this file, restore it to its "
        "original state before starting the task."
    )

    # Final newline check (redundant if content matched, but explicit is nice)
    assert raw_text.endswith("\n"), (
        f"File {RAW_JSON_PATH} must end with a single newline."
    )


def test_output_directories_do_not_exist_yet():
    """The data/ and scripts/ directories must not exist prior to processing."""
    assert not DATA_DIR.exists(), (
        f"Directory {DATA_DIR} should NOT exist before the student starts."
    )
    assert not SCRIPTS_DIR.exists(), (
        f"Directory {SCRIPTS_DIR} should NOT exist before the student starts."
    )


def test_no_derived_files_present():
    """Verify that no task-output files are pre-existing."""
    for path in (CSV_PATH, SUMMARY_JSON_PATH, LOG_PATH):
        assert not path.exists(), (
            f"Derived file {path} should NOT exist before the student starts."
        )