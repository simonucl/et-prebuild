# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the filesystem
_before_ the learner starts working on the “hostname-enrichment” task.

We purposely DO NOT look for any output artefacts; only the presence and
basic integrity of the input data is asserted, so that subsequent tests
can focus on the student’s work.

The checks performed:
1. /home/user/datasets/server_access.csv
   • File exists
   • Has the exact expected header
   • Contains at least one data row
   • All rows have exactly 3 comma-separated columns
2. /home/user/resources/ip_hostname_map.txt
   • File exists
   • Contains at least one mapping row
   • Each row is exactly two fields separated by one <TAB>
   • All IPs referenced in server_access.csv are present in the map
"""

from pathlib import Path
import csv
import pytest

DATASET_PATH = Path("/home/user/datasets/server_access.csv")
MAPPING_PATH = Path("/home/user/resources/ip_hostname_map.txt")


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def read_dataset(path: Path):
    """Return header row (list) and list of data rows (as lists)."""
    with path.open(newline="") as fp:
        reader = csv.reader(fp)
        rows = list(reader)
    header, *data_rows = rows
    return header, data_rows


def read_mapping(path: Path):
    """Return dict mapping IP -> hostname, preserving insertion order."""
    mapping = {}
    with path.open() as fp:
        for lineno, raw in enumerate(fp, 1):
            stripped = raw.rstrip("\n")
            if "\t" not in stripped:
                pytest.fail(
                    f"Line {lineno} in {path} does not contain a tab separator: {stripped!r}"
                )
            ip, host, *rest = stripped.split("\t")
            if rest:
                pytest.fail(
                    f"Line {lineno} in {path} has more than two columns: {stripped!r}"
                )
            if ip in mapping:
                pytest.fail(
                    f"Duplicate IP {ip!r} found in {path} on line {lineno}"
                )
            mapping[ip] = host
    return mapping


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_dataset_exists_and_non_empty():
    assert DATASET_PATH.is_file(), (
        "The source CSV file "
        f"{DATASET_PATH} is missing. It must be present before starting the task."
    )
    assert DATASET_PATH.stat().st_size > 0, (
        f"The source CSV file {DATASET_PATH} is empty."
    )


def test_dataset_header_and_rows():
    header, data_rows = read_dataset(DATASET_PATH)
    expected_header = ["ip", "timestamp", "bytes_sent"]
    assert header == expected_header, (
        f"Unexpected header in {DATASET_PATH}: {header!r}. "
        f"Expected: {expected_header!r}"
    )
    assert data_rows, (
        f"{DATASET_PATH} must contain at least one data row beneath the header."
    )
    for idx, row in enumerate(data_rows, 2):  # start=2 because header is line 1
        assert len(row) == 3, (
            f"Line {idx} in {DATASET_PATH} should contain exactly 3 columns, "
            f"but has {len(row)}: {row!r}"
        )


def test_mapping_exists_and_well_formed():
    assert MAPPING_PATH.is_file(), (
        f"The IP-to-hostname mapping file {MAPPING_PATH} is missing."
    )
    mapping = read_mapping(MAPPING_PATH)
    assert mapping, (
        f"The mapping file {MAPPING_PATH} must contain at least one line."
    )


def test_all_ips_in_dataset_are_mapped():
    _, data_rows = read_dataset(DATASET_PATH)
    dataset_ips = {row[0] for row in data_rows}
    mapping = read_mapping(MAPPING_PATH)
    missing = dataset_ips - mapping.keys()
    assert not missing, (
        "The following IPs from the dataset do not have entries in "
        f"{MAPPING_PATH}: {sorted(missing)}"
    )