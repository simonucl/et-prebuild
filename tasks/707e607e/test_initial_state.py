# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# *before* the student’s solution runs.
#
# It checks that:
#   • /home/user/ir_data exists
#   • The expected input artefacts are present
#   • logs_bundle.zip in that directory contains the three required files
#     with correct headers / structure
#   • Supporting text files are present and contain the expected lines
#   • No solution artefacts have been created yet
#
# Only stdlib + pytest are used.

import json
import os
import zipfile
from pathlib import Path

import pytest

IR_DIR = Path("/home/user/ir_data")
ZIP_PATH = IR_DIR / "logs_bundle.zip"
BLACKLIST_PATH = IR_DIR / "blacklist_ips.txt"
SUSPICIOUS_PROC_PATH = IR_DIR / "suspicious_proc.txt"

EXPECTED_ZIP_CONTENTS = {
    "auth.log.csv",
    "network.log.csv",
    "processes.json",
}

AUTH_HEADER = "timestamp,username,status,source_ip"
NETWORK_HEADER = "timestamp,src_ip,dst_ip,dst_port,protocol"
EXPECTED_BLACKLIST_LINES = {"203.0.113.99", "198.51.100.42"}
EXPECTED_SUSPICIOUS_PROC_LINES = {"nc", "malware_x"}

SUMMARY_DIR = IR_DIR / "summary"
OUTPUT_FILES = {
    "failed_login_counts.csv",
    "blacklisted_connections.csv",
    "suspicious_processes_found.json",
    "incident_report.json",
}


def _read_zip_member(zip_file: zipfile.ZipFile, member: str) -> str:
    """Return member content decoded as UTF-8 with universal newlines."""
    with zip_file.open(member) as fp:
        return fp.read().decode("utf-8", errors="replace").replace("\r\n", "\n")


@pytest.mark.order(1)
def test_ir_directory_exists():
    assert IR_DIR.is_dir(), f"Required directory {IR_DIR} is missing."


@pytest.mark.order(2)
def test_required_files_exist():
    missing = [
        str(p)
        for p in (ZIP_PATH, BLACKLIST_PATH, SUSPICIOUS_PROC_PATH)
        if not p.exists()
    ]
    assert not missing, (
        "The following required file(s) are missing from /home/user/ir_data:\n  "
        + "\n  ".join(missing)
    )


@pytest.mark.order(3)
def test_zip_has_expected_members_and_headers():
    assert ZIP_PATH.is_file(), f"{ZIP_PATH} is not a regular file."

    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = set(zf.namelist())
        assert (
            EXPECTED_ZIP_CONTENTS <= names
        ), f"{ZIP_PATH} is missing expected members: {EXPECTED_ZIP_CONTENTS - names}"

        # --- auth.log.csv ---
        auth_text = _read_zip_member(zf, "auth.log.csv")
        auth_first_line = auth_text.split("\n", 1)[0].strip()
        assert (
            auth_first_line == AUTH_HEADER
        ), f"auth.log.csv header mismatch. Expected '{AUTH_HEADER}', got '{auth_first_line}'."

        # --- network.log.csv ---
        net_text = _read_zip_member(zf, "network.log.csv")
        net_first_line = net_text.split("\n", 1)[0].strip()
        assert (
            net_first_line == NETWORK_HEADER
        ), f"network.log.csv header mismatch. Expected '{NETWORK_HEADER}', got '{net_first_line}'."

        # --- processes.json ---
        processes_raw = _read_zip_member(zf, "processes.json")
        try:
            data = json.loads(processes_raw)
        except json.JSONDecodeError as exc:
            pytest.fail(f"processes.json is not valid JSON: {exc}")

        assert isinstance(
            data, list
        ), "processes.json is expected to be a JSON array (list)."
        assert data, "processes.json should not be empty."
        for idx, item in enumerate(data):
            assert isinstance(item, dict), f"Item #{idx} in processes.json is not an object."
            assert "process_name" in item, f"Item #{idx} missing 'process_name' key."


@pytest.mark.order(4)
def test_blacklist_ips_file_contents():
    with BLACKLIST_PATH.open(encoding="utf-8") as fp:
        lines = {line.strip() for line in fp if line.strip()}

    missing = EXPECTED_BLACKLIST_LINES - lines
    unexpected = lines - EXPECTED_BLACKLIST_LINES
    assert not missing, f"blacklist_ips.txt is missing expected IP(s): {', '.join(sorted(missing))}"
    assert (
        not unexpected
    ), f"blacklist_ips.txt contains unexpected IP(s): {', '.join(sorted(unexpected))}"


@pytest.mark.order(5)
def test_suspicious_proc_file_contents():
    with SUSPICIOUS_PROC_PATH.open(encoding="utf-8") as fp:
        lines = {line.strip() for line in fp if line.strip()}

    missing = EXPECTED_SUSPICIOUS_PROC_LINES - lines
    unexpected = lines - EXPECTED_SUSPICIOUS_PROC_LINES
    assert (
        not missing
    ), f"suspicious_proc.txt is missing expected process name(s): {', '.join(sorted(missing))}"
    assert (
        not unexpected
    ), f"suspicious_proc.txt contains unexpected process name(s): {', '.join(sorted(unexpected))}"


@pytest.mark.order(6)
def test_no_solution_files_exist_yet():
    if SUMMARY_DIR.exists():
        unexpected = [
            f.name for f in SUMMARY_DIR.iterdir() if f.name in OUTPUT_FILES
        ]
        assert (
            not unexpected
        ), "Solution artefacts already exist before the task is run: " + ", ".join(
            sorted(unexpected)
        )