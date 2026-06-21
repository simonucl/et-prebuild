# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
*before* the student performs any work.

Checks performed:
1. /home/user/cloud_usage directory exists.
2. raw_usage.csv exists inside that directory and its contents are **exactly**
   as specified in the public task description.
3. pricing_adjustments.csv exists inside that directory and its contents are
   **exactly** as specified in the public task description.

Only stdlib and pytest are used.  Failures are written so that missing paths or
content mismatches are obvious to the learner.
"""

from pathlib import Path
import pytest

CLOUD_USAGE_DIR = Path("/home/user/cloud_usage")
RAW_USAGE_PATH = CLOUD_USAGE_DIR / "raw_usage.csv"
PRICING_ADJ_PATH = CLOUD_USAGE_DIR / "pricing_adjustments.csv"


@pytest.fixture(scope="module")
def expected_raw_usage_lines():
    return [
        "Service,ResourceID,UsageHours,CostUSD,Region",
        "Compute,i-031,120,48.00,us-east-1",
        "Storage,vol-22,720,36.00,us-east-1",
        "Database,db-67,100,120.00,eu-west-1",
        "Compute,i-099,50,20.00,us-east-1",
        "Analytics,athena-1,30,15.00,us-west-2",
    ]


@pytest.fixture(scope="module")
def expected_pricing_adjustment_lines():
    return [
        "Service,DiscountPercent",
        "Compute,10",
        "Storage,5",
        "Database,15",
        "Analytics,20",
    ]


def test_cloud_usage_directory_exists():
    assert CLOUD_USAGE_DIR.is_dir(), (
        f"Expected directory {CLOUD_USAGE_DIR} to exist, "
        "but it is missing or not a directory."
    )


def _assert_file_exists_and_contents(path: Path, expected_lines):
    assert path.is_file(), f"Expected file {path} to exist, but it is missing."
    try:
        actual_lines = path.read_text().splitlines()
    except Exception as exc:
        pytest.fail(f"Could not read {path}: {exc}")

    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {path} do not match the expected initial state.\n\n"
        "Expected lines:\n"
        + "\n".join(expected_lines)
        + "\n\nActual lines:\n"
        + "\n".join(actual_lines)
    )


def test_raw_usage_file_contents(expected_raw_usage_lines):
    _assert_file_exists_and_contents(RAW_USAGE_PATH, expected_raw_usage_lines)


def test_pricing_adjustments_file_contents(expected_pricing_adjustment_lines):
    _assert_file_exists_and_contents(PRICING_ADJ_PATH, expected_pricing_adjustment_lines)