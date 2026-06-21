# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state
# before the student performs any actions.  It checks that the
# expected cost CSV files are present and that no directories
# or artefacts that will be created during the exercise are
# pre-existing.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")
CLOUD_COSTS = HOME / "cloud_costs"
MONTHLY = CLOUD_COSTS / "monthly"

# ---------------------------------------------------------------------------
# Helper data describing the initial truth
# ---------------------------------------------------------------------------

EXPECTED_CSV_CONTENT = {
    "cost_2023-04.csv": """\
Date,Service,CostUSD
2023-04-30,Compute,123.45
2023-04-30,Storage,67.89
2023-04-30,Network,10.11
""",
    "cost_2023-05.csv": """\
Date,Service,CostUSD
2023-05-31,Compute,150.12
2023-05-31,Storage,70.55
2023-05-31,Network,12.34
""",
    "cost_2023-06.csv": """\
Date,Service,CostUSD
2023-06-30,Compute,131.07
2023-06-30,Storage,72.88
2023-06-30,Network,11.98
""",
    "cost_2023-07.csv": """\
Date,Service,CostUSD
2023-07-31,Compute,142.33
2023-07-31,Storage,75.66
2023-07-31,Network,13.55
""",
}

PROCESSED_DIR = CLOUD_COSTS / "processed"
PER_SERVICE_DIR = CLOUD_COSTS / "per_service"
AUDIT_FILE = CLOUD_COSTS / "link_audit.log"


# ---------------------------------------------------------------------------
# Tests for initial state
# ---------------------------------------------------------------------------

def test_monthly_directory_exists_and_is_directory():
    assert MONTHLY.exists(), f"Directory missing: {MONTHLY}"
    assert MONTHLY.is_dir(), f"Expected {MONTHLY} to be a directory"


def test_expected_csv_files_present_and_only_these():
    csv_files = {p.name for p in MONTHLY.glob("cost_2023-*.csv")}
    expected_files = set(EXPECTED_CSV_CONTENT.keys())
    missing = expected_files - csv_files
    extra = csv_files - expected_files

    assert not missing, (
        "Expected CSV file(s) missing in /home/user/cloud_costs/monthly/: "
        + ", ".join(sorted(missing))
    )
    assert not extra, (
        "Found unexpected CSV file(s) in /home/user/cloud_costs/monthly/: "
        + ", ".join(sorted(extra))
    )


@pytest.mark.parametrize("filename,expected_contents", EXPECTED_CSV_CONTENT.items())
def test_csv_file_contents_match_truth(filename, expected_contents):
    file_path = MONTHLY / filename
    assert file_path.exists(), f"CSV file missing: {file_path}"
    assert file_path.is_file(), f"Not a regular file: {file_path}"

    actual = file_path.read_text()
    # Trim trailing whitespace/newlines for a tolerant comparison.
    assert actual.strip() == expected_contents.strip(), (
        f"Contents of {file_path} do not match expected truth.\n"
        "---- Expected ----\n"
        f"{expected_contents}\n"
        "---- Actual ----\n"
        f"{actual}"
    )


def test_no_processed_or_per_service_dirs_yet():
    assert not PROCESSED_DIR.exists(), (
        f"{PROCESSED_DIR} should NOT exist before the student runs their tasks"
    )
    assert not PER_SERVICE_DIR.exists(), (
        f"{PER_SERVICE_DIR} should NOT exist before the student runs their tasks"
    )


def test_no_audit_file_yet():
    assert not AUDIT_FILE.exists(), (
        f"{AUDIT_FILE} should NOT exist before the student runs their tasks"
    )