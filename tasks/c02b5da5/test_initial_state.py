# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any action.  It checks only the pre-existing CSV
# in /home/user/data/clients.csv and intentionally ignores any output
# artefacts that the assignment will later create.

import csv
from pathlib import Path

CSV_PATH = Path("/home/user/data/clients.csv")


def test_clients_csv_exists():
    """
    The source CSV file must already exist at the exact absolute path.
    """
    assert CSV_PATH.exists(), (
        "Expected the source CSV file to exist at "
        f"{CSV_PATH}, but it was not found."
    )
    assert CSV_PATH.is_file(), (
        f"{CSV_PATH} exists but is not a regular file."
    )


def test_clients_csv_header_is_correct():
    """
    The header row must be exactly:
        id,name,email,status
    with no surrounding spaces.
    """
    with CSV_PATH.open(newline="") as f:
        header_line = f.readline().rstrip("\n\r")
    assert (
        header_line == "id,name,email,status"
    ), (
        "The header row of /home/user/data/clients.csv is incorrect.\n"
        f"Found:    {header_line!r}\n"
        "Expected: 'id,name,email,status'"
    )


def test_clients_csv_has_mixed_status_rows_and_valid_ids():
    """
    Ensure the CSV contains at least one row with status == 'active' and at
    least one row whose status is NOT 'active'.  Also verify that the 'id'
    column contains a valid integer for every row.
    """
    with CSV_PATH.open(newline="") as f:
        reader = csv.DictReader(f)
        active_found = False
        non_active_found = False
        for row_num, row in enumerate(reader, start=2):  # start=2 accounts for header
            # Validate the 'id' column
            assert row["id"].isdigit(), (
                f"Row {row_num}: 'id' should be an integer, found {row['id']!r}."
            )

            status = row["status"]
            assert status == status.lower(), (
                f"Row {row_num}: Status value {status!r} contains uppercase "
                "characters; all statuses should be lowercase."
            )

            if status == "active":
                active_found = True
            else:
                non_active_found = True

    assert active_found, (
        "The CSV must contain at least one row where status == 'active', "
        "but none was found."
    )
    assert non_active_found, (
        "The CSV should have at least one row where status is not 'active' "
        "to allow meaningful filtering, but none was found."
    )