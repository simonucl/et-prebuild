# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem / data state
for the “Merge CSV data, apply date-filter, convert to JSON …” task.

These tests make sure the provided input artefacts are present and
contain the exact expected content *before* the student starts working.
No assertions are made about any output paths—only the required inputs.
"""

from pathlib import Path
import pytest

# Base directories
BASE_DIR = Path("/home/user/projects/api_test")
INPUT_DIR = BASE_DIR / "input"

# Absolute input paths
ORDERS_CSV = INPUT_DIR / "orders.csv"
CUSTOMERS_CSV = INPUT_DIR / "customers.csv"

# Expected file contents (without trailing newline characters)
EXPECTED_ORDERS_LINES = [
    "order_id,customer_id,order_date,amount",
    "1001,C001,2023-01-05,250.75",
    "1002,C002,2023-01-17,400.00",
    "1003,C001,2023-02-03,125.50",
    "1004,C003,2023-03-12,98.00",
]

EXPECTED_CUSTOMERS_LINES = [
    "customer_id,name,country",
    "C001,Alice Smith,USA",
    "C002,Bob Jones,Canada",
    "C003,Carla Ruiz,Mexico",
]


def _read_non_empty_lines(path: Path):
    """
    Helper that reads the file, strips CR/LF endings and removes a
    possible final blank line so comparisons are stable.
    """
    with path.open("r", encoding="utf-8") as fp:
        lines = [ln.rstrip("\r\n") for ln in fp.readlines()]
    # Remove a single trailing blank line, if present.
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def test_input_directory_exists():
    assert INPUT_DIR.is_dir(), (
        f"Required directory not found: {INPUT_DIR}. "
        "The task expects the input CSVs to be located here."
    )


@pytest.mark.parametrize(
    "csv_path, expected_lines, label",
    [
        (ORDERS_CSV, EXPECTED_ORDERS_LINES, "orders.csv"),
        (CUSTOMERS_CSV, EXPECTED_CUSTOMERS_LINES, "customers.csv"),
    ],
)
def test_csv_files_exist_and_match_expected(csv_path: Path, expected_lines, label):
    # 1. Presence
    assert csv_path.is_file(), f"Missing required input file: {csv_path}"

    # 2. Readability
    try:
        actual_lines = _read_non_empty_lines(csv_path)
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"Could not read {label} as UTF-8: {exc}"
        )

    # 3. Content equality
    assert actual_lines == expected_lines, (
        f"Content of {label} does not match the expected fixture.\n"
        f"Expected:\n{expected_lines}\n\nActual:\n{actual_lines}"
    )