# test_initial_state.py
#
# This pytest suite validates that the **pre-existing** input data needed for
# the security-report task is present and correct.  It intentionally *does not*
# check for the output directory or file the student will create later.
#
# The tests verify:
#   1. The scan_data directory exists.
#   2. kernel.txt exists and contains exactly one non-empty line.
#   3. port_scan.log exists and includes the three required port/protocol
#      combinations (22/tcp, 8080/tcp, 68/udp) in the expected order.
#   4. sshd_config exists and contains exactly one “PermitRootLogin” line whose
#      value is “yes”.
#
# Any failure message should clearly indicate which prerequisite item is
# missing or malformed.

from pathlib import Path
import pytest

SCAN_DIR = Path("/home/user/scan_data")
KERNEL_FILE = SCAN_DIR / "kernel.txt"
PORT_SCAN_FILE = SCAN_DIR / "port_scan.log"
SSHD_CONFIG_FILE = SCAN_DIR / "sshd_config"


def test_scan_data_directory_exists():
    assert SCAN_DIR.is_dir(), f"Required directory {SCAN_DIR} does not exist."


def test_kernel_file_content():
    assert KERNEL_FILE.is_file(), f"Required file {KERNEL_FILE} is missing."
    lines = KERNEL_FILE.read_text(encoding="utf-8").splitlines()
    assert lines, f"{KERNEL_FILE} is empty."
    assert len(lines) == 1, (
        f"{KERNEL_FILE} should contain exactly one line, found {len(lines)}."
    )
    kernel_version = lines[0].strip()
    assert kernel_version == "5.15.0-test", (
        f"Unexpected kernel version in {KERNEL_FILE!s}: "
        f"expected '5.15.0-test', found '{kernel_version}'."
    )


def test_port_scan_log_contains_required_ports():
    assert PORT_SCAN_FILE.is_file(), f"Required file {PORT_SCAN_FILE} is missing."
    content = PORT_SCAN_FILE.read_text(encoding="utf-8").splitlines()

    # Extract only the data lines after the header (anything that starts with 'tcp' or 'udp')
    data_lines = [line for line in content if line.strip().startswith(("tcp", "udp"))]
    assert data_lines, f"No data lines found in {PORT_SCAN_FILE}."

    required_ports = ["0.0.0.0:22", "0.0.0.0:8080", "0.0.0.0:68"]
    found_ports = []

    for line in data_lines:
        # Simple substring search is adequate for this audit.
        for port in required_ports:
            if port in line:
                found_ports.append(port)

    missing = [p for p in required_ports if p not in found_ports]
    assert not missing, (
        f"The following required ports were not found in {PORT_SCAN_FILE}: {', '.join(missing)}"
    )

    # Verify order (22/tcp, 8080/tcp, 68/udp) appears top-to-bottom.
    indices = [next(i for i, l in enumerate(data_lines) if port in l) for port in required_ports]
    assert indices == sorted(indices), (
        f"Ports are present but not in the required order (22/tcp, 8080/tcp, 68/udp) "
        f"in {PORT_SCAN_FILE}."
    )


def test_sshd_config_permit_root_login_line():
    assert SSHD_CONFIG_FILE.is_file(), f"Required file {SSHD_CONFIG_FILE} is missing."
    lines = SSHD_CONFIG_FILE.read_text(encoding="utf-8").splitlines()

    permit_lines = [
        l.strip() for l in lines if l.strip().startswith("PermitRootLogin")
    ]
    assert permit_lines, (
        f"{SSHD_CONFIG_FILE} does not contain a 'PermitRootLogin' directive."
    )
    assert len(permit_lines) == 1, (
        f"{SSHD_CONFIG_FILE} should contain exactly one 'PermitRootLogin' line, "
        f"found {len(permit_lines)}."
    )

    # The directive is expected to be of the form: "PermitRootLogin <value>"
    parts = permit_lines[0].split()
    assert len(parts) == 2, (
        f"Malformed 'PermitRootLogin' line in {SSHD_CONFIG_FILE}: '{permit_lines[0]}'"
    )
    value = parts[1]
    assert value == "yes", (
        f"Unexpected value for 'PermitRootLogin' in {SSHD_CONFIG_FILE}: "
        f"expected 'yes', found '{value}'."
    )