# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem is in the
# expected **initial** state *before* the student performs any work.
#
# It intentionally makes NO assertions about the output directory or files
# that the student will create later (/home/user/reports/…); those paths are
# out of scope for an “initial state” check.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Expected immutable values for the raw firewall CSV                          #
# --------------------------------------------------------------------------- #

CSV_PATH = Path("/home/user/logs/fw-incident-20240612.csv")

EXPECTED_CSV_CONTENT = (
    "timestamp,src_ip,dst_ip,protocol,action,bytes\n"
    "2024-06-12T08:55:01Z,10.0.0.15,172.16.0.1,ICMP,Blocked,0\n"
    "2024-06-12T09:01:17Z,192.168.1.22,172.16.0.5,TCP,Allowed,1500\n"
    "2024-06-12T09:02:45Z,203.0.113.45,172.16.0.7,TCP,Blocked,0\n"
    "2024-06-12T09:05:30Z,198.51.100.12,172.16.0.9,UDP,Blocked,0\n"
)


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #

def _read_file_bytes(path: Path) -> bytes:
    """Read file contents as raw bytes."""
    with path.open("rb") as fh:
        return fh.read()


def _read_file_text(path: Path) -> str:
    """Read file contents using UTF-8 (strict)."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_logs_directory_exists():
    logs_dir = CSV_PATH.parent
    assert logs_dir.is_dir(), (
        f"Required directory {logs_dir} is missing or not a directory."
    )


def test_csv_file_exists_and_is_regular():
    assert CSV_PATH.exists(), (
        f"Expected CSV file {CSV_PATH} does not exist."
    )
    assert CSV_PATH.is_file(), (
        f"Path {CSV_PATH} exists but is not a regular file."
    )


def test_csv_file_is_utf8_readable():
    """Opening the file with UTF-8 must not raise a UnicodeDecodeError."""
    try:
        _ = _read_file_text(CSV_PATH)
    except UnicodeDecodeError as exc:
        pytest.fail(f"CSV file {CSV_PATH} is not valid UTF-8: {exc}")


def test_csv_file_contents_exact_match():
    actual = _read_file_text(CSV_PATH)
    assert actual == EXPECTED_CSV_CONTENT, (
        f"Contents of {CSV_PATH} do not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{EXPECTED_CSV_CONTENT!r}\n"
        "---- Actual ----\n"
        f"{actual!r}"
    )


def test_csv_file_final_newline():
    raw_bytes = _read_file_bytes(CSV_PATH)
    assert raw_bytes.endswith(b"\n"), (
        f"CSV file {CSV_PATH} must end with exactly one trailing newline."
    )