# test_initial_state.py
#
# Pytest suite that validates the operating‐system state *before* the
# student starts working on the task.  It checks only the items that are
# guaranteed to exist prior to any user action and deliberately ignores
# all required output artefacts (/home/user/report, etc.).

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
SCANS_DIR = HOME / "scans"
OPEN_PORTS = SCANS_DIR / "open_ports.csv"
VULNS = SCANS_DIR / "vulns.csv"


@pytest.mark.parametrize(
    "path_to_check, expected_type",
    [
        (SCANS_DIR, "dir"),
        (OPEN_PORTS, "file"),
        (VULNS, "file"),
    ],
)
def test_paths_exist(path_to_check: Path, expected_type: str):
    """
    Ensure the required directory and CSV files exist in their absolute
    locations *before* the student begins work.
    """
    assert path_to_check.exists(), f"Required {expected_type} {path_to_check} is missing."
    if expected_type == "dir":
        assert path_to_check.is_dir(), f"{path_to_check} should be a directory."
    else:
        assert path_to_check.is_file(), f"{path_to_check} should be a regular file."


def _check_permissions(path: Path, expected_mode: int):
    """
    Helper that verifies POSIX permissions (mask is compared to the
    lowest 3 octal digits—e.g. 0o755 or 0o644).
    """
    mode = path.stat().st_mode & 0o777
    assert mode == expected_mode, (
        f"{path} should have permissions {oct(expected_mode)} "
        f"but has {oct(mode)} instead."
    )


def test_directory_permissions():
    _check_permissions(SCANS_DIR, 0o755)


@pytest.mark.parametrize("csv_file, expected_mode", [(OPEN_PORTS, 0o644), (VULNS, 0o644)])
def test_file_permissions(csv_file: Path, expected_mode: int):
    _check_permissions(csv_file, expected_mode)


def test_open_ports_content():
    """
    Validate exact content (header + 4 data rows, trailing newline) for open_ports.csv.
    """
    expected_lines = [
        "IP,Port,Protocol,Service\n",
        "192.168.1.10,22,tcp,ssh\n",
        "192.168.1.10,80,tcp,http\n",
        "192.168.1.20,445,tcp,smb\n",
        "192.168.1.20,3389,tcp,rdp\n",
    ]

    with OPEN_PORTS.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    assert lines == expected_lines, (
        f"{OPEN_PORTS} content is not as expected.\n"
        f"Expected lines:\n{''.join(expected_lines)}\n"
        f"Actual lines:\n{''.join(lines)}"
    )
    # Extra safety: ensure only 5 lines are present
    assert len(lines) == 5, f"{OPEN_PORTS} should contain exactly 5 lines, found {len(lines)}."


def test_vulns_content():
    """
    Validate exact content (header + 4 data rows, trailing newline) for vulns.csv.
    """
    expected_lines = [
        "Service,CVE,Severity\n",
        "ssh,CVE-2018-15473,High\n",
        "smb,CVE-2020-0796,Critical\n",
        "http,CVE-2021-26855,High\n",
        "rdp,CVE-2019-0708,Critical\n",
    ]

    with VULNS.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    assert lines == expected_lines, (
        f"{VULNS} content is not as expected.\n"
        f"Expected lines:\n{''.join(expected_lines)}\n"
        f"Actual lines:\n{''.join(lines)}"
    )
    # Extra safety: ensure only 5 lines are present
    assert len(lines) == 5, f"{VULNS} should contain exactly 5 lines, found {len(lines)}."