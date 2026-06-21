# test_initial_state.py
#
# This pytest suite validates that the operating-system / file-system
# starts in the expected pristine state **before** the student begins
# the FinOps analysis task.

import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pytest

# ---------- Constants ---------- #
HOME_DIR = Path("/home/user")
RAW_DIR = HOME_DIR / "cloud_usage" / "raw_logs"

COMPUTE_CSV = RAW_DIR / "compute_jan.csv"
STORAGE_CSV = RAW_DIR / "storage_jan.csv"

EXPECTED_COMPUTE_LINES = [
    "Service,InstanceType,Hours,HourlyCostUSD",
    "EC2,m5.large,200,0.096",
    "EC2,c5.xlarge,150,0.17",
    "Lambda,GB-Seconds,3000000,0.00001667",
]

EXPECTED_STORAGE_LINES = [
    "Service,GB-Months,CostPerGBMonthUSD",
    "S3 Standard,500,0.023",
    "S3 Glacier,200,0.004",
]

# Pre-computed truth values based on the raw CSV contents
EXPECTED_TOTAL_COMPUTE_SPEND = Decimal("94.71")   # USD
EXPECTED_TOTAL_STORAGE_SPEND = Decimal("12.30")   # USD
EXPECTED_EC2_SPEND          = Decimal("44.70")    # USD (used for later savings)
EXPECTED_S3_LIFECYCLE_SAVING = Decimal("1.90")    # USD (100 GB migration)


# ---------- Helper Functions ---------- #
def read_csv_lines(path: Path):
    """Return the list of stripped lines (without trailing newlines)."""
    with path.open(newline="") as fh:
        return [line.rstrip("\n") for line in fh]


def decimal_round(value: Decimal) -> Decimal:
    """Round a Decimal to two places using ROUND_HALF_UP (financial)."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ---------- Tests ---------- #
def test_raw_logs_directory_exists():
    assert RAW_DIR.is_dir(), (
        f"Expected directory {RAW_DIR} to exist "
        "so that raw CSV usage files can be read."
    )


def test_compute_csv_presence_and_contents():
    assert COMPUTE_CSV.is_file(), f"Missing file: {COMPUTE_CSV}"
    lines = read_csv_lines(COMPUTE_CSV)
    assert lines == EXPECTED_COMPUTE_LINES, (
        f"{COMPUTE_CSV} does not match expected contents. "
        "Check headers, row order, and values."
    )


def test_storage_csv_presence_and_contents():
    assert STORAGE_CSV.is_file(), f"Missing file: {STORAGE_CSV}"
    lines = read_csv_lines(STORAGE_CSV)
    assert lines == EXPECTED_STORAGE_LINES, (
        f"{STORAGE_CSV} does not match expected contents. "
        "Check headers, row order, and values."
    )


def test_calculated_spend_matches_expected():
    # Compute spend from compute_jan.csv
    with COMPUTE_CSV.open(newline="") as fh:
        reader = csv.DictReader(fh)
        total_compute = Decimal("0")
        ec2_spend = Decimal("0")
        for row in reader:
            hours = Decimal(row["Hours"])
            cost_per_hour = Decimal(row["HourlyCostUSD"])
            service_cost = hours * cost_per_hour
            total_compute += service_cost
            if row["Service"] == "EC2":
                ec2_spend += service_cost

    # Storage spend from storage_jan.csv
    with STORAGE_CSV.open(newline="") as fh:
        reader = csv.DictReader(fh)
        total_storage = Decimal("0")
        for row in reader:
            gb_months = Decimal(row["GB-Months"])
            cost_per_gb = Decimal(row["CostPerGBMonthUSD"])
            total_storage += gb_months * cost_per_gb

    # Round totals to cents
    total_compute = decimal_round(total_compute)
    total_storage = decimal_round(total_storage)
    ec2_spend = decimal_round(ec2_spend)

    # Assertions
    assert total_compute == EXPECTED_TOTAL_COMPUTE_SPEND, (
        f"Computed total compute spend {total_compute} USD does not match "
        f"expected {EXPECTED_TOTAL_COMPUTE_SPEND} USD. "
        "Verify the numbers in compute_jan.csv."
    )

    assert total_storage == EXPECTED_TOTAL_STORAGE_SPEND, (
        f"Computed total storage spend {total_storage} USD does not match "
        f"expected {EXPECTED_TOTAL_STORAGE_SPEND} USD. "
        "Verify the numbers in storage_jan.csv."
    )

    assert ec2_spend == EXPECTED_EC2_SPEND, (
        f"Calculated EC2 spend {ec2_spend} USD does not match "
        f"expected {EXPECTED_EC2_SPEND} USD."
    )

    # Validate S3 lifecycle saving amount derived from 100 GB migration
    price_std = Decimal("0.023")
    price_glacier = Decimal("0.004")
    lifecycle_saving = decimal_round(Decimal("100") * (price_std - price_glacier))
    assert lifecycle_saving == EXPECTED_S3_LIFECYCLE_SAVING, (
        f"Calculated S3 lifecycle saving {lifecycle_saving} USD does not match "
        f"expected {EXPECTED_S3_LIFECYCLE_SAVING} USD."
    )