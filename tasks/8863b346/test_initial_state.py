# test_initial_state.py
#
# This pytest suite verifies that the *initial* filesystem state is
# exactly as described in the task specification.  It purposely does
# NOT check for any of the output artefacts that the student is
# expected to create later on.

import os
import pytest
import csv

CLOUD_DIR = "/home/user/cloud"
INVENTORY_CSV = os.path.join(CLOUD_DIR, "inventory.csv")

# The inventory is expected to contain six LF-terminated lines exactly as
# spelled out below (the trailing \n on the last line is mandatory).
EXPECTED_INVENTORY_CONTENT = (
    "ServiceName,OldServer,NewServer,Owner\n"
    "auth-api,vm-auth-01,vm-auth-02,becky\n"
    "billing-db,vm-db-08,vm-db-new,rahul\n"
    "frontend,vm-fe-03,vm-fe-blue,carla\n"
    "metrics,vm-mt-01,vm-mt-02,becky\n"
    "search,vm-sr-12,vm-sr-green,rahul\n"
)


def test_cloud_directory_exists():
    """The /home/user/cloud directory must already exist."""
    assert os.path.isdir(CLOUD_DIR), (
        f"Required directory {CLOUD_DIR!r} is missing.  "
        "It must be present before any work begins."
    )


def test_inventory_csv_exists():
    """The inventory.csv file must already be present."""
    assert os.path.isfile(INVENTORY_CSV), (
        f"Required inventory file {INVENTORY_CSV!r} is missing.  "
        "It must be in place before the migration starts."
    )


def test_inventory_csv_exact_content():
    """
    The inventory.csv file must match the expected six-line content *exactly*,
    including header row, ordering, separators, and trailing newline.
    """
    with open(INVENTORY_CSV, "r", encoding="utf-8", newline="") as fh:
        data = fh.read()

    assert data == EXPECTED_INVENTORY_CONTENT, (
        "inventory.csv content does not match the expected specification.\n\n"
        "Expected:\n"
        f"{EXPECTED_INVENTORY_CONTENT!r}\n\n"
        "Found:\n"
        f"{data!r}"
    )


def test_inventory_csv_parses_correctly():
    """
    As a sanity check, verify that the CSV can be parsed and that the header
    as well as each data row contains exactly four columns.
    """
    with open(INVENTORY_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    # There must be exactly one header + five data rows.
    assert len(rows) == 6, (
        f"inventory.csv should contain 6 rows (1 header + 5 data), "
        f"but {len(rows)} rows were found."
    )

    expected_header = ["ServiceName", "OldServer", "NewServer", "Owner"]
    assert rows[0] == expected_header, (
        "Header row in inventory.csv is incorrect.\n"
        f"Expected: {expected_header}\nFound:    {rows[0]}"
    )

    for idx, row in enumerate(rows[1:], start=2):
        assert len(row) == 4, (
            f"Row {idx} in inventory.csv does not have exactly 4 comma-"
            f"separated fields: {row}"
        )