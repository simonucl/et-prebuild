# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem
state **before** the student attempts the exercise.

Only stdlib + pytest are used, per instructions.
"""

import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants – absolute paths that must already exist on the VM
# ---------------------------------------------------------------------------
HOME = Path("/home/user")
DATA_DIR = HOME / "data"
AUDIT_DIR = HOME / "audit"
TX_FILE = DATA_DIR / "transactions.json"
SCHEMA_FILE = DATA_DIR / "transaction_schema.json"
AUDIT_LOG = AUDIT_DIR / "audit.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def read_json(path: Path):
    """Read and return JSON from *path*, raising an explicit assertion if it
    cannot be parsed."""
    assert path.exists(), f"Expected file at {path} does not exist."
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}")


# ---------------------------------------------------------------------------
# Tests for required directories & files
# ---------------------------------------------------------------------------
def test_data_directory_exists():
    assert DATA_DIR.is_dir(), f"Directory {DATA_DIR} is expected to exist."


def test_transactions_file_exists():
    assert TX_FILE.is_file(), f"File {TX_FILE} is expected to exist."


def test_schema_file_exists():
    assert SCHEMA_FILE.is_file(), f"File {SCHEMA_FILE} is expected to exist."


def test_audit_log_does_not_yet_exist():
    """
    Before the student runs their solution, the audit.log file must NOT
    exist. It will be created during the task.
    """
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} already exists, but it should be generated only by the "
        "student's solution."
    )


# ---------------------------------------------------------------------------
# Content validation for transactions.json
# ---------------------------------------------------------------------------
def test_transactions_file_content():
    data = read_json(TX_FILE)

    # Must be a list with exactly 3 elements.
    assert isinstance(data, list), f"{TX_FILE} must contain a JSON array."
    assert len(data) == 3, f"{TX_FILE} must contain exactly 3 records."

    # Collect IDs for further checks
    ids = {obj.get("id") for obj in data}
    expected_ids = {"TX1001", "TX1002", "TX1003"}
    assert ids == expected_ids, (
        f"{TX_FILE} should contain records with IDs "
        f"{', '.join(sorted(expected_ids))}."
    )

    # Individual record checks
    record_by_id = {obj["id"]: obj for obj in data}

    # TX1001 – compliant
    tx1 = record_by_id["TX1001"]
    assert tx1.get("amount") == 150.00, "TX1001 amount should be 150.00"
    assert tx1.get("currency") == "USD", "TX1001 currency should be USD"
    assert tx1.get("status") == "approved", "TX1001 status should be approved"

    # TX1002 – missing status (non-compliant)
    tx2 = record_by_id["TX1002"]
    assert "status" not in tx2, "TX1002 must be missing 'status' to be non-compliant."

    # TX1003 – compliant but declined
    tx3 = record_by_id["TX1003"]
    assert tx3.get("amount") == 99.99, "TX1003 amount should be 99.99"
    assert tx3.get("currency") == "USD", "TX1003 currency should be USD"
    assert tx3.get("status") == "declined", "TX1003 status should be declined"


# ---------------------------------------------------------------------------
# Content validation for transaction_schema.json
# ---------------------------------------------------------------------------
def test_schema_file_content():
    schema = read_json(SCHEMA_FILE)

    # Basic structure checks
    assert isinstance(schema, dict), f"{SCHEMA_FILE} must contain a JSON object."

    # Required keys list must match exactly
    required = schema.get("required")
    assert required is not None, f"{SCHEMA_FILE} must contain a 'required' field."
    expected_required = ["id", "amount", "currency", "status"]
    assert sorted(required) == sorted(
        expected_required
    ), f"'required' field in {SCHEMA_FILE} must be {expected_required}"