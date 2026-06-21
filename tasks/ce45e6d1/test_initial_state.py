# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state for the FinOps cost-analysis exercise.  These tests must all pass
# *before* the student starts working.  They purposely fail as soon as any
# of the required artefacts (venv, scripts, logs, etc.) already exist, or
# if the provided AWS Cost & Usage CSV is missing / malformed.
#
# No third-party libraries are used—only stdlib + pytest.

import csv
import os
from pathlib import Path

HOME = Path("/home/user")
CLOUD_DIR = HOME / "cloud_data"
CSV_PATH = CLOUD_DIR / "cost_data.csv"
VENV_DIR = HOME / "finops_venv"
ANALYZE_SCRIPT = CLOUD_DIR / "analyze_costs.py"
SUMMARY_LOG = CLOUD_DIR / "cloud_costs_summary.log"
REQ_FILE = CLOUD_DIR / "requirements.txt"


def test_cost_data_csv_exists_and_is_readable():
    assert CSV_PATH.exists(), (
        f"Expected CSV file not found at {CSV_PATH}. "
        "It must be present before any work begins."
    )
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a file."

    # Basic sanity check: file is non-empty and first line has the expected header
    with CSV_PATH.open("r", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        assert header == ["Service", "Date", "CostUSD"], (
            "The header of cost_data.csv is incorrect. "
            f"Expected ['Service','Date','CostUSD'] but got {header}"
        )

        rows = list(reader)
        assert len(rows) == 8, (
            f"Unexpected number of data rows. Expected 8, got {len(rows)}."
        )

        # Verify all required services are present and costs parse as floats
        services_seen = set()
        for svc, _date, cost in rows:
            services_seen.add(svc)
            # Ensure cost can be parsed to float
            try:
                float(cost)
            except ValueError:
                pytest.fail(f"Cost value '{cost}' in {CSV_PATH} is not a valid float.")

        for svc in {"EC2", "S3", "RDS"}:
            assert (
                svc in services_seen
            ), f"Service '{svc}' missing from {CSV_PATH}. Found: {services_seen}"


def test_no_preexisting_virtual_environment():
    assert not VENV_DIR.exists(), (
        f"The virtual environment directory {VENV_DIR} already exists. "
        "The learner must create it during the exercise, not beforehand."
    )


def test_no_analysis_script_yet():
    assert not ANALYZE_SCRIPT.exists(), (
        f"Found {ANALYZE_SCRIPT} but it should not exist before the exercise starts."
    )


def test_no_summary_log_yet():
    assert not SUMMARY_LOG.exists(), (
        f"Found {SUMMARY_LOG} but it should not exist before the exercise starts."
    )


def test_no_requirements_file_yet():
    assert not REQ_FILE.exists(), (
        f"Found {REQ_FILE} but it should not exist before the exercise starts."
    )


def test_no_pycache_in_cloud_data():
    pycache_dirs = [
        p for p in CLOUD_DIR.rglob("__pycache__") if p.is_dir()
    ]
    assert not pycache_dirs, (
        "__pycache__ directories found under /home/user/cloud_data before "
        "the exercise has begun: " + ", ".join(str(p) for p in pycache_dirs)
    )