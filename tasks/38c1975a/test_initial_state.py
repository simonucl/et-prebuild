# test_initial_state.py
#
# Pytest suite that verifies the **pre-seeded** filesystem and environment
# before the student executes their shell command.
#
# The tests purposely avoid looking for any artefacts that should be produced
# by the student (e.g. /home/user/report or its files).  They only confirm
# that the starting conditions described in the task are indeed satisfied.
#
# The assertions include:
#   • presence / absence of specific paths
#   • file contents for the two JSON files
#   • basic JSON structure / types
#   • availability of the “jq” executable in $PATH
#
# All failure messages are explicit so students immediately know what part of
# the initial state is broken if a test fails.

import json
import os
import stat
import textwrap
import shutil
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
REPORT_DIR = os.path.join(HOME, "report")
INVENTORY_JSON = os.path.join(DATA_DIR, "inventory.json")
SCHEMA_JSON = os.path.join(DATA_DIR, "inventory_schema.json")

@pytest.fixture(scope="session")
def inventory_text():
    """Read /home/user/data/inventory.json exactly as bytes -> str."""
    if not os.path.isfile(INVENTORY_JSON):
        pytest.skip("inventory.json missing – remaining tests depend on it")
    with open(INVENTORY_JSON, "r", encoding="utf-8") as fh:
        return fh.read()

@pytest.fixture(scope="session")
def inventory_json(inventory_text):
    """Parsed JSON content of inventory.json"""
    try:
        return json.loads(inventory_text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"inventory.json is not valid JSON: {exc}")

def test_data_directory_exists():
    assert os.path.isdir(DATA_DIR), f"Expected directory {DATA_DIR!r} to exist"

def test_inventory_files_exist():
    for path in (INVENTORY_JSON, SCHEMA_JSON):
        assert os.path.isfile(path), f"Required file {path!r} is missing"

def test_report_directory_absent():
    assert not os.path.exists(
        REPORT_DIR
    ), f"{REPORT_DIR!r} should NOT exist before the student command runs"

def test_permissions_on_data_dir():
    mode = os.stat(DATA_DIR).st_mode
    expected = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH  # 0o755
    assert (
        mode & 0o777 == expected
    ), f"{DATA_DIR} should have 0755 permissions, found {oct(mode & 0o777)}"

def test_inventory_json_exact_text(inventory_text):
    # Exact canonical content expected in the task description
    expected = textwrap.dedent(
        """
        {
          "warehouse": "central",
          "items": [
            {"id":101,"name":"blue widget","quantity":5},
            {"id":102,"name":"red widget","quantity":25},
            {"id":203,"name":"green gizmo","quantity":7},
            {"id":304,"name":"yellow gizmo","quantity":12}
          ]
        }
        """
    ).lstrip()
    assert (
        inventory_text == expected
    ), "inventory.json content differs from the expected pre-seeded data"

def test_inventory_json_structure(inventory_json):
    """
    In addition to exact-text check above, ensure basic structure so that
    later student 'jq' validation has something sensible to run against.
    """
    assert isinstance(
        inventory_json, dict
    ), "inventory.json should contain a JSON object at the top level"
    assert "warehouse" in inventory_json, "Key 'warehouse' missing from inventory.json"
    assert "items" in inventory_json, "Key 'items' missing from inventory.json"
    assert isinstance(
        inventory_json["warehouse"], str
    ), "Value of 'warehouse' should be a string"
    items = inventory_json["items"]
    assert isinstance(items, list), "'items' should be an array"
    # Validate each item has the required keys and types
    for idx, itm in enumerate(items):
        assert isinstance(itm, dict), f"items[{idx}] is not an object"
        for key, typ in (("id", int), ("name", str), ("quantity", int)):
            assert key in itm, f"Key '{key}' missing in items[{idx}]"
            assert isinstance(
                itm[key], typ
            ), f"items[{idx}]['{key}'] expected type {typ.__name__}"
        assert (
            itm["quantity"] >= 0
        ), f"items[{idx}]['quantity'] must be non-negative"

def test_schema_file_is_valid_json():
    with open(SCHEMA_JSON, "r", encoding="utf-8") as fh:
        try:
            json.load(fh)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{SCHEMA_JSON} is not valid JSON: {exc}")

def test_jq_available_in_path():
    jq_path = shutil.which("jq")
    assert jq_path is not None, "Executable 'jq' must be available in $PATH for the task"