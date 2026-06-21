# test_initial_state.py
#
# This pytest suite verifies that the starting filesystem state is present
# and correct *before* the student performs any actions.  It checks only the
# inputs that must already exist and deliberately avoids looking for any of
# the artefacts the student is expected to create (e.g. the
# /home/user/network_diagnostics/ directory or port-map.log).

import os
import re
import pytest
from pathlib import Path

HOME = Path("/home/user")
MICROSERVICES_DIR = HOME / "microservices"

# --------------------------------------------------------------------------- #
# Helper data describing the expected YAML snippets                           #
# --------------------------------------------------------------------------- #
EXPECTED_YAMLS = {
    "auth-service.yaml": {
        "container_name": "auth-service",
        "host_port": "8001",
        "container_port": "8000",
    },
    "billing-service.yaml": {
        "container_name": "billing-service",
        "host_port": "8002",
        "container_port": "8000",
    },
    "notification-service.yaml": {
        "container_name": "notification-service",
        "host_port": "8003",
        "container_port": "8000",
    },
}


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_microservices_directory_exists():
    """The /home/user/microservices/ directory must exist."""
    assert MICROSERVICES_DIR.is_dir(), (
        f"Required directory {MICROSERVICES_DIR} is missing. "
        "The three Compose snippets must live here."
    )


@pytest.mark.parametrize("filename", list(EXPECTED_YAMLS.keys()))
def test_compose_file_exists(filename):
    """Each expected Compose snippet must exist as a file."""
    path = MICROSERVICES_DIR / filename
    assert path.is_file(), f"Expected Compose file {path} is missing."


@pytest.mark.parametrize(
    "filename,expectations", EXPECTED_YAMLS.items(), ids=list(EXPECTED_YAMLS.keys())
)
def test_compose_file_core_contents(filename, expectations):
    """
    Verify that each Compose snippet includes at least:
      • the correct container_name
      • a ports mapping in the form "HOST:CONTAINER"
    We do *not* attempt full YAML parsing to keep dependencies minimal.
    """
    path = MICROSERVICES_DIR / filename
    text = path.read_text(encoding="utf-8")

    # 1. container_name line
    cn_pattern = rf"\bcontainer_name:\s*{re.escape(expectations['container_name'])}\b"
    assert re.search(
        cn_pattern, text
    ), f"{path}: missing or incorrect container_name '{expectations['container_name']}'."

    # 2. ports mapping line
    port_pair = f"{expectations['host_port']}:{expectations['container_port']}"
    ports_pattern = rf'["\']?{re.escape(port_pair)}["\']?'
    assert re.search(
        ports_pattern, text
    ), (
        f"{path}: expected ports mapping '{port_pair}' not found. "
        "Ensure the YAML contains the correct host:container port pair."
    )