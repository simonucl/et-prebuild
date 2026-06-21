# test_initial_state.py
#
# This test-suite validates the filesystem *before* the student’s migration
# script is executed.  It confirms that the raw input necessary for the task
# exists and is exactly as described in the specification.  Nothing about the
# expected output artefacts is asserted here ‑ the student has not run yet.
#
# Rules honoured:
#   • Only stdlib + pytest are used.
#   • Absolute paths are checked.
#   • No assertions are made about any “output” or “logs” files / directories.

import pathlib
import pytest
import csv

BASE_DIR = pathlib.Path("/home/user/cloud_migration")
SOURCE_DIR = BASE_DIR / "source"
SERVICES_CSV = SOURCE_DIR / "services.csv"

# --------------------------------------------------------------------------- #
# Expected canonical content of services.csv (with trailing newlines stripped)
# --------------------------------------------------------------------------- #
EXPECTED_CSV_LINES = [
    "service_name,node,port,protocol,status",
    "auth-api,edge-1,443,https,active",
    "billing-api,edge-2,443,https,active",
    "legacy-report,node-5,8080,http,inactive",
    "user-db,edge-1,5432,postgres,active",
    "cache,node-3,6379,redis,maintenance",
    "frontend,node-2,80,http,active",
    "search,node-2,9200,http,active",
]


def test_source_directory_exists_and_is_dir():
    assert SOURCE_DIR.exists(), (
        f"Required source directory {SOURCE_DIR} is missing."
    )
    assert SOURCE_DIR.is_dir(), (
        f"{SOURCE_DIR} exists but is not a directory."
    )


def test_services_csv_present_and_is_file():
    assert SERVICES_CSV.exists(), (
        f"Input CSV file {SERVICES_CSV} is missing."
    )
    assert SERVICES_CSV.is_file(), (
        f"{SERVICES_CSV} exists but is not a regular file."
    )


def test_services_csv_exact_content():
    # Read file and normalise newline endings by stripping only the end-of-line
    # characters, leaving the interior commas and spacing intact.
    with SERVICES_CSV.open("r", encoding="utf-8") as fp:
        lines = [line.rstrip("\n\r") for line in fp.readlines()]

    assert lines == EXPECTED_CSV_LINES, (
        "Content of services.csv does not exactly match the expected "
        "pre-populated data.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_CSV_LINES)
        + "\n\nActual:\n"
        + "\n".join(lines)
    )


def test_services_csv_semantics():
    """
    Sanity-check the parsed CSV:

    • Exactly eight rows: one header + seven data rows.
    • The header columns match the specification in correct order.
    • The counts of status values are as described (5 active, 1 inactive,
      1 maintenance).
    """
    with SERVICES_CSV.open(newline="", encoding="utf-8") as fp:
        reader = list(csv.DictReader(fp))

    # Row count (excluding header)
    assert len(reader) == 7, (
        f"Expected 7 data rows in services.csv, found {len(reader)}."
    )

    # Header verification
    expected_header = [
        "service_name",
        "node",
        "port",
        "protocol",
        "status",
    ]
    assert reader[0].keys() == dict.fromkeys(expected_header).keys(), (
        "CSV header columns do not match expected order: "
        f"{', '.join(expected_header)}"
    )

    # Status distribution
    status_counts = {}
    for row in reader:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1

    assert status_counts.get("active", 0) == 5, (
        "There should be exactly 5 rows with status 'active'. "
        f"Found: {status_counts.get('active', 0)}."
    )
    assert status_counts.get("inactive", 0) == 1, (
        "There should be exactly 1 row with status 'inactive'. "
        f"Found: {status_counts.get('inactive', 0)}."
    )
    assert status_counts.get("maintenance", 0) == 1, (
        "There should be exactly 1 row with status 'maintenance'. "
        f"Found: {status_counts.get('maintenance', 0)}."
    )