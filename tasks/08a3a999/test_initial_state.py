# test_initial_state.py
#
# This pytest suite verifies that the *initial* operating-system state
# is exactly what the student hand-out promises — no more and no less.
# It intentionally avoids checking for *output* artefacts that the
# student is expected to create later (e.g. /home/user/incidents/**).
#
# What we *do* check:
#   • The directory /home/user/source_data exists.
#   • The files /home/user/source_data/servers.csv and events.csv exist,
#     are regular files, are non-empty, and contain the exact header
#     rows and data rows stated in the task description.
#
# Only Python’s standard library and pytest are used.


import csv
import os
from pathlib import Path

import pytest

SOURCE_DIR = Path("/home/user/source_data")
SERVERS_CSV = SOURCE_DIR / "servers.csv"
EVENTS_CSV = SOURCE_DIR / "events.csv"


@pytest.fixture(scope="module")
def servers_rows():
    """Load and return rows from servers.csv as a list of OrderedDicts."""
    with SERVERS_CSV.open(newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


@pytest.fixture(scope="module")
def events_rows():
    """Load and return rows from events.csv as a list of OrderedDicts."""
    with EVENTS_CSV.open(newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def test_source_data_directory_exists():
    assert SOURCE_DIR.exists(), (
        f"Required directory {SOURCE_DIR} is missing. "
        "The incident-response drill cannot proceed without it."
    )
    assert SOURCE_DIR.is_dir(), f"{SOURCE_DIR} exists but is not a directory."


def test_servers_csv_present_and_readable():
    assert SERVERS_CSV.exists(), (
        f"Expected CSV file {SERVERS_CSV} is missing. "
        "It should have been staged for the student."
    )
    assert SERVERS_CSV.is_file(), f"{SERVERS_CSV} exists but is not a regular file."
    assert os.access(SERVERS_CSV, os.R_OK), f"{SERVERS_CSV} is not readable."
    assert SERVERS_CSV.stat().st_size > 0, f"{SERVERS_CSV} is empty."


def test_events_csv_present_and_readable():
    assert EVENTS_CSV.exists(), (
        f"Expected CSV file {EVENTS_CSV} is missing. "
        "It should have been staged for the student."
    )
    assert EVENTS_CSV.is_file(), f"{EVENTS_CSV} exists but is not a regular file."
    assert os.access(EVENTS_CSV, os.R_OK), f"{EVENTS_CSV} is not readable."
    assert EVENTS_CSV.stat().st_size > 0, f"{EVENTS_CSV} is empty."


def test_servers_csv_header_and_rows(servers_rows):
    expected_header = ["id", "hostname", "status"]
    with SERVERS_CSV.open(newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
    assert header == expected_header, (
        f"Header of {SERVERS_CSV} is {header!r}; expected {expected_header!r}."
    )

    expected_rows = [
        {"id": "1", "hostname": "web-01", "status": "up"},
        {"id": "2", "hostname": "db-01", "status": "up"},
        {"id": "3", "hostname": "cache-01", "status": "down"},
    ]
    assert servers_rows == expected_rows, (
        f"Contents of {SERVERS_CSV} do not match expectation.\n"
        f"Expected:\n  {expected_rows!r}\n"
        f"Actual:\n  {servers_rows!r}"
    )


def test_events_csv_header_and_rows(events_rows):
    expected_header = ["id", "server_id", "timestamp", "description"]
    with EVENTS_CSV.open(newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
    assert header == expected_header, (
        f"Header of {EVENTS_CSV} is {header!r}; expected {expected_header!r}."
    )

    expected_rows = [
        {"id": "101", "server_id": "1", "timestamp": "2023-01-12 10:15:00", "description": "Deployment"},
        {"id": "102", "server_id": "3", "timestamp": "2023-01-12 10:16:00", "description": "Cache restart"},
        {"id": "103", "server_id": "3", "timestamp": "2023-01-12 11:00:00", "description": "Cache down"},
        {"id": "104", "server_id": "3", "timestamp": "2023-01-12 11:05:00", "description": "Cache still down"},
        {"id": "105", "server_id": "2", "timestamp": "2023-01-12 11:10:00", "description": "DB maintenance"},
        {"id": "106", "server_id": "1", "timestamp": "2023-01-12 12:00:00", "description": "Deployment complete"},
    ]
    assert events_rows == expected_rows, (
        f"Contents of {EVENTS_CSV} do not match expectation.\n"
        f"Expected:\n  {expected_rows!r}\n"
        f"Actual:\n  {events_rows!r}"
    )