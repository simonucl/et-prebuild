# test_initial_state.py
#
# Pytest suite that validates the pristine filesystem *before* the
# student begins any work.  It checks that the two required source
# files exist with the exact expected content and that none of the
# output artefacts or their directories have been created yet.
#
# Only the Python standard library and pytest are used.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def read_text(path: pathlib.Path) -> str:
    """Read a text file and return its contents.

    Raises a helpful AssertionError if the file is missing.
    """
    assert path.exists(), f"Expected file missing: {path}"
    assert path.is_file(), f"Expected a regular file, but found something else: {path}"
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


def lines_without_newlines(text: str):
    """Return a list of lines *without* their trailing newline characters."""
    return text.splitlines()


def assert_trailing_newline(path: pathlib.Path, raw_bytes: bytes):
    """Ensure the very last byte in the file is '\n' (Linux line-ending)."""
    assert raw_bytes.endswith(b"\n"), (
        f"{path} must end with a single LF newline (\\n).  "
        "No CRLF (\\r\\n) or missing trailing newline is allowed."
    )


def assert_equal_iterable(got, expected, context: str):
    """Assert two iterables have exactly the same members and order."""
    assert list(got) == list(expected), (
        f"Content mismatch in {context}.\n"
        f"Expected:\n{expected!r}\nGot:\n{list(got)!r}"
    )


# ---------------------------------------------------------------------------
# Expected reference data
# ---------------------------------------------------------------------------

REG_CSV_PATH = HOME / "configs" / "registration.csv"
FW_TSV_PATH = HOME / "changes" / "firmware_versions.tsv"

MATRIX_TSV_PATH = HOME / "reports" / "config_change_matrix.tsv"
LOG_PATH = HOME / "logs" / "column_extraction.log"

EXPECTED_REG_LINES = [
    "server_id;location;role;maint_window",
    "srv01;us-east;web;Sun 01:00",
    "srv02;us-west;db;Mon 02:00",
    "srv03;eu-central;cache;Tue 03:00",
]

EXPECTED_FW_LINES = [
    "server_id\tversion\trelease_date",
    "srv01\t1.2.4\t2024-01-21",
    "srv02\t1.4.7\t2024-02-10",
    "srv03\t1.3.2\t2024-02-28",
]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_registration_csv_exists_and_has_expected_content():
    raw = REG_CSV_PATH.read_bytes()  # Need the raw bytes for newline check
    assert_trailing_newline(REG_CSV_PATH, raw)

    text = raw.decode("utf-8")
    lines = lines_without_newlines(text)
    assert_equal_iterable(lines, EXPECTED_REG_LINES, str(REG_CSV_PATH))

    # Ensure semicolon is the only delimiter present.
    for i, line in enumerate(lines[1:], 2):  # skip header, human-friendly line numbers start at 1
        assert ";" in line, f"{REG_CSV_PATH}: expected ';' in data line {i}"
        assert "\t" not in line, f"{REG_CSV_PATH}: found TAB in line {i}, should be semicolon-separated"

    # Column count should be exactly four per line.
    for i, line in enumerate(lines, 1):
        cols = line.split(";")
        assert len(cols) == 4, (
            f"{REG_CSV_PATH}: line {i} should have exactly 4 semicolon-separated columns "
            f"but has {len(cols)}: {cols}"
        )


def test_firmware_versions_tsv_exists_and_has_expected_content():
    raw = FW_TSV_PATH.read_bytes()
    assert_trailing_newline(FW_TSV_PATH, raw)

    text = raw.decode("utf-8")
    lines = lines_without_newlines(text)
    assert_equal_iterable(lines, EXPECTED_FW_LINES, str(FW_TSV_PATH))

    # Ensure tab is the only delimiter present.
    for i, line in enumerate(lines[1:], 2):
        assert "\t" in line, f"{FW_TSV_PATH}: expected TAB in data line {i}"
        assert ";" not in line, f"{FW_TSV_PATH}: found semicolon in line {i}, should be TAB-separated"

    # Column count should be exactly three per line.
    for i, line in enumerate(lines, 1):
        cols = line.split("\t")
        assert len(cols) == 3, (
            f"{FW_TSV_PATH}: line {i} should have exactly 3 tab-separated columns "
            f"but has {len(cols)}: {cols}"
        )


def test_output_directories_and_files_do_not_exist_yet():
    # None of the target artefacts should exist before the student runs their solution.
    assert not MATRIX_TSV_PATH.exists(), (
        f"{MATRIX_TSV_PATH} already exists — the consolidation script has "
        "apparently been executed prematurely."
    )
    assert not LOG_PATH.exists(), (
        f"{LOG_PATH} already exists — the verification log should be generated "
        "only after the student runs their solution."
    )

    # Directories may or may not exist at this point; if they do, they must be empty.
    reports_dir = MATRIX_TSV_PATH.parent
    logs_dir = LOG_PATH.parent

    for d in (reports_dir, logs_dir):
        if d.exists():
            assert d.is_dir(), f"{d} exists but is not a directory"
            contents = [p for p in d.iterdir()]
            assert not contents, (
                f"Directory {d} should be empty before the task is attempted, "
                f"but contains: {', '.join(map(str, contents))}"
            )