# test_initial_state.py
#
# This suite verifies the *initial* state of the VM **before** the student
# starts working.  It checks only the files that must already be present.
# It purposely avoids looking for any output-related artefacts the student
# is expected to create later.
#
# Run with:  pytest -q
#
# NOTE:  Only stdlib + pytest are used, per requirements.

import os
import stat
import csv
import textwrap
import pytest
from pathlib import Path

HOME = Path("/home/user")
PROJECT_DIR = HOME / "capacity_planner"
USAGE_CSV = PROJECT_DIR / "usage.csv"
BASELINE_RULES = PROJECT_DIR / "baseline_firewall.rules"


@pytest.mark.describe("Pre-existing directory structure")
def test_project_directory_exists_and_is_directory():
    assert PROJECT_DIR.exists(), f"Missing directory: {PROJECT_DIR}"
    assert PROJECT_DIR.is_dir(), f"{PROJECT_DIR} exists but is not a directory"


@pytest.mark.describe("usage.csv presence and exact content")
def test_usage_csv_exists_with_expected_content():
    expected = textwrap.dedent("""\
        service,port,avg_cpu,avg_mem_MB,avg_network_Mbps
        http,80,25,512,120
        https,443,30,600,150
        ssh,22,5,100,5
        postgres,5432,10,800,30
        redis,6379,8,200,20
        prometheus,9090,15,300,40
        """)
    # Ensure final newline is present
    if not expected.endswith("\n"):
        expected += "\n"

    assert USAGE_CSV.is_file(), f"Expected file not found: {USAGE_CSV}"

    actual = USAGE_CSV.read_text()
    assert actual == expected, (
        f"{USAGE_CSV} content mismatch.\n--- Expected ---\n{expected}\n--- Actual ---\n{actual}"
    )


@pytest.mark.describe("baseline_firewall.rules presence and exact content")
def test_baseline_firewall_rules_exists_with_expected_content():
    expected = textwrap.dedent("""\
        -A INPUT -p tcp --dport 22 -j ACCEPT
        -A INPUT -p tcp --dport 80 -j ACCEPT
        -A INPUT -p tcp --dport 443 -j ACCEPT
        -A INPUT -j DROP
        """)
    if not expected.endswith("\n"):
        expected += "\n"

    assert BASELINE_RULES.is_file(), f"Expected file not found: {BASELINE_RULES}"

    actual = BASELINE_RULES.read_text()
    assert actual == expected, (
        f"{BASELINE_RULES} content mismatch.\n--- Expected ---\n{expected}\n--- Actual ---\n{actual}"
    )


@pytest.mark.describe("usage.csv numeric parsing and expected ranking")
def test_top_three_services_computed_correctly():
    expected_ranking = [
        ("https", 443, 150),
        ("http", 80, 120),
        ("prometheus", 9090, 40),
    ]

    with open(USAGE_CSV, newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    # Convert numeric fields
    for row in rows:
        row["avg_network_Mbps"] = int(row["avg_network_Mbps"])
        row["port"] = int(row["port"])

    # Sort by avg_network_Mbps descending
    rows_sorted = sorted(rows, key=lambda r: r["avg_network_Mbps"], reverse=True)
    top_three = [(r["service"], r["port"], r["avg_network_Mbps"]) for r in rows_sorted[:3]]

    assert top_three == expected_ranking, (
        "Computed top-three services do not match expected ranking.\n"
        f"Expected: {expected_ranking}\nGot:      {top_three}"
    )


@pytest.mark.describe("File permissions are reasonable (world-readable)")
@pytest.mark.parametrize("path", [USAGE_CSV, BASELINE_RULES])
def test_initial_files_are_world_readable(path: Path):
    mode = path.stat().st_mode
    is_world_readable = bool(mode & stat.S_IROTH)
    assert is_world_readable, f"{path} must be world-readable (mode 644 or less restrictive)"