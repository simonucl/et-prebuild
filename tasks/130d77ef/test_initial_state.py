# test_initial_state.py
#
# This pytest suite validates that the initial support-case staging area is
# present *before* the student creates the diagnostics bundle.  It confirms
# the existence and correctness of all source files that the student is
# expected to read from, but it deliberately avoids checking for any of the
# output artefacts the student must create.

import os
import pathlib
import pytest

# ----------  CONSTANTS  ------------------------------------------------------

BASE_DIR = pathlib.Path("/home/user/support_case")

AUTH_LOG               = BASE_DIR / "auth.log"
MOCK_SS_OUTPUT         = BASE_DIR / "mock_ss_output.txt"
SSH_CONFIG             = BASE_DIR / "etc" / "ssh" / "sshd_config"
PASSWD_FILE            = BASE_DIR / "etc" / "passwd"

EXPECTED_FAILED_COUNT  = 3
EXPECTED_TCP_PORTS     = [22, 80, 5432]
EXPECTED_SIZES         = {
    SSH_CONFIG: 54,
    PASSWD_FILE: 75,
}

# ----------  HELPERS  --------------------------------------------------------

def _read_text(path: pathlib.Path) -> str:
    """Read and return the full text of a file."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}", pytrace=False)


# ----------  TESTS  ----------------------------------------------------------

def test_auth_log_failed_password_count():
    """
    The auth.log file must exist and contain exactly three lines with the
    phrase 'Failed password'.
    """
    assert AUTH_LOG.is_file(), f"Missing required file: {AUTH_LOG}"

    text = _read_text(AUTH_LOG)
    failed_lines = [line for line in text.splitlines() if "Failed password" in line]
    assert len(failed_lines) == EXPECTED_FAILED_COUNT, (
        "auth.log should contain exactly "
        f"{EXPECTED_FAILED_COUNT} lines with 'Failed password', "
        f"but found {len(failed_lines)}.\n"
        "Offending file contents:\n" + text
    )


def test_mock_ss_output_tcp_listen_ports():
    """
    The mock_ss_output.txt file must exist and list the correct unique TCP
    LISTEN ports (22, 80, 5432) in any order.
    """
    assert MOCK_SS_OUTPUT.is_file(), f"Missing required file: {MOCK_SS_OUTPUT}"

    lines = _read_text(MOCK_SS_OUTPUT).splitlines()
    if not lines:
        pytest.fail(f"{MOCK_SS_OUTPUT} is empty.", pytrace=False)

    ports = set()
    for line in lines[1:]:                           # skip header
        columns = line.split()
        if len(columns) < 5:
            continue
        if columns[0] == "tcp" and columns[1] == "LISTEN":
            local_addr = columns[4]                 # e.g., '0.0.0.0:22'
            if ":" in local_addr:
                port_str = local_addr.rsplit(":", 1)[-1]
                if port_str.isdigit():
                    ports.add(int(port_str))

    sorted_ports = sorted(ports)
    assert sorted_ports == EXPECTED_TCP_PORTS, (
        "Expected TCP LISTEN ports to be "
        f"{EXPECTED_TCP_PORTS}, but found {sorted_ports}.\n"
        "Parsed from file:\n" + "\n".join(lines)
    )


@pytest.mark.parametrize("path,expected_size", EXPECTED_SIZES.items())
def test_file_sizes(path: pathlib.Path, expected_size: int):
    """
    Verify the exact byte sizes of sshd_config and passwd source files.
    """
    assert path.is_file(), f"Missing required file: {path}"
    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, (
        f"File {path} should be {expected_size} bytes, but is {actual_size} bytes."
    )