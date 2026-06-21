# test_initial_state.py
#
# Pytest suite that verifies the **initial** filesystem / OS state
# before the student starts working on the task.
#
# The checks purposefully avoid touching any output artefacts that
# the student is expected to create (validation.log, outdated_kernels.log).
#
# Only the stdlib and pytest are used, in accordance with the rules.

import json
import re
from pathlib import Path

SERVER_DATA_DIR = Path("/home/user/server_data")
INVENTORY_JSON = SERVER_DATA_DIR / "inventory.json"
SCHEMA_JSON = SERVER_DATA_DIR / "inventory_schema.json"

RE_IP = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


def load_json(path: Path):
    """Utility: read and parse JSON from *path*."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:  # pragma: no cover
        raise AssertionError(f"Expected file '{path}' to exist but it does not.")
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise AssertionError(f"The file '{path}' is not valid JSON:\n{exc}")


def test_server_data_directory_exists():
    assert SERVER_DATA_DIR.is_dir(), (
        f"Required directory '{SERVER_DATA_DIR}' is missing.  "
        "It must be present before the student starts."
    )


def test_required_files_exist():
    for file_path in (INVENTORY_JSON, SCHEMA_JSON):
        assert file_path.is_file(), (
            f"Required file '{file_path}' is missing.  "
            "It must be present before the student starts."
        )


def test_inventory_json_structure_and_content():
    data = load_json(INVENTORY_JSON)

    # Top-level type / key check
    assert isinstance(data, dict), (
        f"'{INVENTORY_JSON}' must contain a JSON object at the top level."
    )
    assert "servers" in data, (
        f"'{INVENTORY_JSON}' must contain a top-level key called 'servers'."
    )
    servers = data["servers"]
    assert isinstance(servers, list), "'servers' must be a JSON array."

    # Check each server entry
    required_keys = {"hostname", "ip", "kernel", "os_release"}
    for idx, srv in enumerate(servers):
        assert isinstance(srv, dict), (
            f"Element #{idx} in 'servers' must be a JSON object."
        )
        missing = required_keys - srv.keys()
        assert not missing, (
            f"Element #{idx} in 'servers' is missing required keys: {sorted(missing)}"
        )
        # Basic sanity checks on individual fields
        assert isinstance(srv["hostname"], str) and srv["hostname"], (
            f"Element #{idx}: 'hostname' must be a non-empty string."
        )
        assert RE_IP.match(srv["ip"]), (
            f"Element #{idx}: 'ip' value '{srv['ip']}' is not a valid IPv4 address."
        )
        assert isinstance(srv["kernel"], str) and srv["kernel"], (
            f"Element #{idx}: 'kernel' must be a non-empty string."
        )
        assert isinstance(srv["os_release"], str) and srv["os_release"], (
            f"Element #{idx}: 'os_release' must be a non-empty string."
        )


def test_expected_outdated_kernel_hostnames():
    """
    There should be exactly the two servers whose kernel *major*
    version is lower than 5.  This guarantees that the fixture
    matches the reference answer expected by the grader.
    """
    data = load_json(INVENTORY_JSON)
    servers = data["servers"]

    def major(kernel_str: str) -> int:
        # Kernel strings look like '5.15.0-60-generic' or '4.19.0-17-amd64'
        return int(kernel_str.split(".", 1)[0])

    outdated = sorted(
        srv["hostname"] for srv in servers if major(srv["kernel"]) < 5
    )

    expected = ["db-01", "legacy-01"]
    assert outdated == expected, (
        "The set of servers with a kernel major version lower than 5 "
        f"must be {expected}.  Got: {outdated}"
    )