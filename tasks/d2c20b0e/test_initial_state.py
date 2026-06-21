# test_initial_state.py
#
# This pytest suite validates that all prerequisite artefacts are present
# and correctly structured *before* the student script is executed.
#
# It intentionally does NOT test for the presence of any output files or
# directories that will be produced by the student solution.

import json
import csv
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
CONTAINERS_BASE = HOME / "containers"
VULN_CSV = HOME / "vuln_db" / "vuln_ports.csv"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Failed to parse JSON file at {path}: {exc}")


def _read_csv(path: Path):
    try:
        with path.open(newline="") as fp:
            return list(csv.reader(fp))
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Failed to parse CSV file at {path}: {exc}")

# --------------------------------------------------------------------------- #
# Tests for container bundles
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("container_dir", "expected_ports"),
    [
        ("proxy",  {"80/tcp", "443/tcp", "8080/tcp"}),
        ("api",    {"3000/tcp", "22/tcp"}),
    ],
)
def test_container_bundle_exists_and_has_expected_ports(container_dir, expected_ports):
    """
    Ensure each OCI-layout container bundle exists and advertises the expected ports.
    """
    directory = CONTAINERS_BASE / container_dir
    assert directory.is_dir(), (
        f"Required directory missing: {directory}"
    )

    json_path = directory / "container.json"
    assert json_path.is_file(), (
        f"Required file missing: {json_path}"
    )

    data = _read_json(json_path)

    # Navigate to Config → ExposedPorts
    try:
        exposed_ports = data["Config"]["ExposedPorts"]
    except KeyError as exc:  # pragma: no cover
        pytest.fail(
            f"container.json at {json_path} is missing key {exc}; "
            "expected structure: Config → ExposedPorts → {...}"
        )

    actual_ports = set(exposed_ports.keys())
    # Ports must match exactly—no extras, no omissions.
    assert actual_ports == expected_ports, (
        f"ExposedPorts for {container_dir} do not match the specification.\n"
        f"Expected: {sorted(expected_ports)}\n"
        f"Actual:   {sorted(actual_ports)}"
    )

# --------------------------------------------------------------------------- #
# Tests for vulnerability CSV
# --------------------------------------------------------------------------- #
def test_vulnerability_csv_exists_and_is_well_formed():
    """
    Verify that the vulnerability CSV exists, is readable, has the correct
    header, contains the expected rows, and has unique port numbers.
    """
    assert VULN_CSV.is_file(), (
        f"Required CSV missing: {VULN_CSV}"
    )

    # Basic POSIX readability check (owner, group, others)
    mode = VULN_CSV.stat().st_mode
    is_readable = any(
        mode & perm for perm in (stat.S_IRUSR, stat.S_IRGRP, stat.S_IROTH)
    )
    assert is_readable, (
        f"CSV file {VULN_CSV} exists but is not world-readable."
    )

    rows = _read_csv(VULN_CSV)
    assert rows, "CSV file is empty."

    header = rows[0]
    expected_header = ["Port", "Service", "Severity"]
    assert header == expected_header, (
        f"CSV header mismatch. Expected {expected_header}, got {header}"
    )

    # Convert remaining rows into dict keyed by port for uniqueness checks
    data_rows = rows[1:]
    assert data_rows, "CSV must contain at least one data row."

    ports_seen = set()
    for idx, row in enumerate(data_rows, start=2):  # start=2 because of header
        assert len(row) == 3, (
            f"Row {idx} in CSV does not have exactly 3 columns: {row}"
        )
        port_str, service, severity = row
        # Validate port
        assert port_str.isdigit(), (
            f"Port value '{port_str}' in row {idx} is not an integer."
        )
        port_int = int(port_str)
        # Ensure uniqueness
        assert port_int not in ports_seen, (
            f"Duplicate port '{port_int}' found in CSV row {idx}."
        )
        ports_seen.add(port_int)
        # Basic non-empty checks
        assert service, f"Service column is empty in row {idx}."
        assert severity, f"Severity column is empty in row {idx}."

    # Check that the expected vulnerable ports are present
    expected_ports = {22, 80, 443, 3000, 8080}
    assert expected_ports <= ports_seen, (
        "CSV is missing one or more required ports.\n"
        f"Expected ports: {sorted(expected_ports)}\n"
        f"Actual ports:   {sorted(ports_seen)}"
    )