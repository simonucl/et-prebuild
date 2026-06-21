# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem state is exactly
# what the student instructions describe.  It checks only the *input* assets
# (raw datasets) and deliberately avoids touching any of the “clean” output
# paths, in accordance with the grading-environment guidelines.

import json
from pathlib import Path

RAW_DIR = Path("/home/user/datasets/raw")
TRANSACTIONS_CSV = RAW_DIR / "transactions.csv"
USERS_JSON = RAW_DIR / "users.json"


def test_raw_directory_exists():
    """The raw-data directory must be present and be a directory."""
    assert RAW_DIR.exists(), f"Required directory missing: {RAW_DIR}"
    assert RAW_DIR.is_dir(), f"Expected {RAW_DIR} to be a directory."


def test_transactions_csv_presence_and_basic_shape():
    """
    Validate presence of the raw CSV and ensure it has exactly the
    header + 6 data records (7 lines total).
    """
    assert TRANSACTIONS_CSV.exists(), f"Required file missing: {TRANSACTIONS_CSV}"
    assert TRANSACTIONS_CSV.is_file(), f"{TRANSACTIONS_CSV} should be a regular file."

    lines = TRANSACTIONS_CSV.read_text(encoding="utf-8").splitlines()
    expected_line_count = 7  # 1 header + 6 rows
    assert (
        len(lines) == expected_line_count
    ), f"{TRANSACTIONS_CSV} should have {expected_line_count} lines, found {len(lines)}."

    header = "transaction_id,date,amount,user_id,currency"
    assert (
        lines[0] == header
    ), f"CSV header mismatch.\nExpected: {header!r}\nFound   : {lines[0]!r}"

    # Sanity-check for key idiosyncrasies that the cleaning step relies on.
    assert any(
        ",," in line for line in lines[1:]
    ), "No row with a blank user_id found; expected at least one."
    assert any(
        ",usd" in line.lower() for line in lines[1:]
    ), "No row with lowercase 'usd' currency found; expected at least one."
    assert lines.count(lines[2]) > 1, (
        "A duplicate row is expected in the raw CSV but was not detected; "
        "the cleaning spec relies on its presence."
    )


def test_users_json_presence_and_basic_shape():
    """
    Validate presence of the raw JSON and ensure it is a list with exactly
    five user objects, including one missing 'email' and a duplicate user_id.
    """
    assert USERS_JSON.exists(), f"Required file missing: {USERS_JSON}"
    assert USERS_JSON.is_file(), f"{USERS_JSON} should be a regular file."

    try:
        data = json.loads(USERS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise AssertionError(f"{USERS_JSON} is not valid JSON: {exc}") from exc

    assert isinstance(
        data, list
    ), f"{USERS_JSON} should contain a JSON array, found {type(data).__name__}."

    expected_count = 5
    assert (
        len(data) == expected_count
    ), f"JSON array should have {expected_count} elements, found {len(data)}."

    # Confirm at least one object is missing the 'email' field.
    if not any("email" not in obj for obj in data):
        raise AssertionError(
            "Expected at least one user object without an 'email' field."
        )

    # Confirm there is a duplicate user_id (specifically 504).
    user_id_counts = {}
    for obj in data:
        uid = obj.get("user_id")
        user_id_counts[uid] = user_id_counts.get(uid, 0) + 1

    duplicates = [uid for uid, count in user_id_counts.items() if count > 1]
    assert (
        duplicates
    ), "Expected at least one duplicate user_id in the raw JSON, found none."
    assert 504 in duplicates, "Expected user_id 504 to appear at least twice."