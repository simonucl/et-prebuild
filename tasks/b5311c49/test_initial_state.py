# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before* the
# student performs any action for the “jq one-liner” task.
#
# Rules enforced:
#   • Only standard-library modules are used.
#   • We test *only* for pre-existing artefacts.
#   • Output artefacts (e.g. /home/user/disk_validation.log) are NOT checked here.

import json
import os
import stat
import pytest

# Constants
INVENTORY_PATH = "/home/user/disk_inventory.json"
REQUIRED_KEYS = {
    "mount",
    "size_gb",
    "used_gb",
    "available_gb",
    "percent_used",
}


def test_disk_inventory_file_exists():
    """
    The machine-generated inventory file must already be present.
    """
    assert os.path.exists(INVENTORY_PATH), (
        f"The required file {INVENTORY_PATH} does not exist. "
        "It must be present *before* you start the task."
    )
    assert os.path.isfile(INVENTORY_PATH), (
        f"{INVENTORY_PATH} exists but is not a regular file."
    )

    # Sanity-check basic permissions: file should be readable by the user.
    file_mode = os.stat(INVENTORY_PATH).st_mode
    is_readable = bool(file_mode & stat.S_IRUSR)
    assert is_readable, f"{INVENTORY_PATH} is not readable by the current user."


def _load_inventory():
    """
    Helper: load and return the JSON content of the inventory file.
    Provides a clear pytest failure message if anything goes wrong.
    """
    try:
        with open(INVENTORY_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"{INVENTORY_PATH} is not valid JSON: {exc}",
            pytrace=False,
        )


def test_inventory_structure_and_schema():
    """
    Validate that the JSON is an array where every element contains *exactly*
    the required five keys with appropriate data types and value ranges.
    """
    data = _load_inventory()

    assert isinstance(data, list), (
        f"{INVENTORY_PATH} must contain a JSON array at the top level."
    )
    assert data, f"{INVENTORY_PATH} contains an empty array; at least one entry is required."

    for idx, entry in enumerate(data):
        # Basic type check
        assert isinstance(entry, dict), (
            f"Element #{idx} in {INVENTORY_PATH} is not a JSON object."
        )

        # Key check: exactly the required keys, no more, no less
        entry_keys = set(entry.keys())
        missing = REQUIRED_KEYS - entry_keys
        extra = entry_keys - REQUIRED_KEYS
        assert not missing, (
            f"Element #{idx} is missing required keys: {', '.join(sorted(missing))}"
        )
        assert not extra, (
            f"Element #{idx} contains unexpected keys: {', '.join(sorted(extra))}"
        )

        # Field-by-field validation
        mount = entry["mount"]
        size_gb = entry["size_gb"]
        used_gb = entry["used_gb"]
        available_gb = entry["available_gb"]
        percent_used = entry["percent_used"]

        assert isinstance(mount, str) and mount, (
            f"Element #{idx}: 'mount' must be a non-empty string."
        )

        for field_name, value, allow_zero in [
            ("size_gb", size_gb, False),
            ("used_gb", used_gb, True),
            ("available_gb", available_gb, True),
        ]:
            assert isinstance(value, int), (
                f"Element #{idx}: '{field_name}' must be an integer."
            )
            if allow_zero:
                assert value >= 0, (
                    f"Element #{idx}: '{field_name}' must be ≥ 0."
                )
            else:
                assert value > 0, (
                    f"Element #{idx}: '{field_name}' must be > 0."
                )

        assert isinstance(percent_used, int), (
            f"Element #{idx}: 'percent_used' must be an integer."
        )
        assert 0 <= percent_used <= 100, (
            f"Element #{idx}: 'percent_used' must be between 0 and 100 inclusive."
        )