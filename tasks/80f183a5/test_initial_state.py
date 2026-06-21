# test_initial_state.py
#
# Pytest suite that validates the machine *before* the learner’s solution
# is executed.  It confirms that the prerequisite file is present with the
# correct contents, that the expected output file is still absent, and that
# the real-world network reachability of the three test IP addresses matches
# the ground-truth described in the assignment.
#
# Only Python’s stdlib and pytest are used.

from pathlib import Path
import shutil
import subprocess
import sys
import pytest


IP_LIST_PATH = Path("/home/user/ip_list.txt")
REPORT_PATH = Path("/home/user/connectivity_report.log")

EXPECTED_IP_LINES = [
    "8.8.8.8\n",
    "1.1.1.1\n",
    "192.0.2.1\n",
]

# Ground-truth reachability for the grading environment
REACHABILITY_EXPECTATIONS = {
    "8.8.8.8": True,
    "1.1.1.1": True,
    "192.0.2.1": False,
}


def _skip_if_ping_missing():
    """Skip the entire module if the system lacks a usable `ping` binary."""
    if shutil.which("ping") is None:
        pytest.skip("'ping' utility not found on this system; "
                    "cannot perform reachability checks.",
                    allow_module_level=True)


def test_ip_list_file_exists_and_has_expected_content():
    """Verify /home/user/ip_list.txt exists and contains the exact expected text."""
    assert IP_LIST_PATH.exists(), (
        "Prerequisite file /home/user/ip_list.txt is missing."
    )
    assert IP_LIST_PATH.is_file(), (
        "/home/user/ip_list.txt exists but is not a regular file."
    )

    # Read with trailing newlines preserved for a byte-for-byte comparison.
    with IP_LIST_PATH.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert lines == EXPECTED_IP_LINES, (
        "Contents of /home/user/ip_list.txt are incorrect.\n"
        f"Expected:\n{''.join(EXPECTED_IP_LINES)!r}\n"
        f"Found:\n{''.join(lines)!r}"
    )


def test_connectivity_report_not_present_yet():
    """
    The output file must not exist before the learner has run their solution.
    Presence here would indicate leftover artefacts from a previous run.
    """
    assert not REPORT_PATH.exists(), (
        "/home/user/connectivity_report.log already exists, "
        "but it should only be created by the learner's solution."
    )


@pytest.mark.parametrize("ip, expected_up", REACHABILITY_EXPECTATIONS.items())
def test_actual_icmp_reachability_matches_expectations(ip, expected_up):
    """
    Send exactly one ICMP echo request (-c 1) with a one-second deadline (-W 1)
    to each IP and verify that the observed reachability matches the ground truth.
    """
    _skip_if_ping_missing()

    cmd = ["ping", "-n", "-c", "1", "-W", "1", ip]
    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    is_up = result.returncode == 0
    assert is_up == expected_up, (
        f"Reachability for {ip} is expected to be "
        f"{'UP' if expected_up else 'DOWN'}, "
        f"but the probe reported it as {'UP' if is_up else 'DOWN'}."
    )