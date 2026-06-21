# test_initial_state.py
#
# This pytest suite verifies that the execution environment is in the
# expected “clean” state *before* the student begins the assignment.
#
# What we check:
#   1. The target CSV file that the student must create is NOT present.
#   2. Basic name-resolution inside the container works for:
#        • “localhost”  → must resolve to 127.0.0.1
#        • the machine’s current short hostname
#
# These guarantees allow the real grading tests (run **after** the
# student’s work) to behave deterministically.

from pathlib import Path
import os
import socket
import subprocess
import pytest

# Fixed paths used in the assignment
FINOPS_DIR = Path("/home/user/finops")
CSV_FILE   = FINOPS_DIR / "dns_resolution_report.csv"


def test_csv_file_absent_before_student_starts():
    """
    The CSV file must NOT exist before the student starts working.
    If it is already present the environment is polluted and the real
    grading tests would produce false positives/negatives.
    """
    assert not CSV_FILE.exists(), (
        f"Pre-check failed: {CSV_FILE} already exists. "
        "The workspace must start in a clean state."
    )


def test_localhost_resolves_to_loopback():
    """
    Sanity-check that the container’s resolver maps 'localhost'
    to the IPv4 loopback address 127.0.0.1.
    """
    try:
        ip = socket.gethostbyname("localhost")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Name resolution for 'localhost' failed: {exc}")

    assert ip == "127.0.0.1", (
        f"'localhost' resolved to {ip!r}, but 127.0.0.1 was expected. "
        "The container’s /etc/hosts or DNS configuration seems wrong."
    )


def _get_short_hostname() -> str:
    """
    Return the system's **short** hostname (no domain part).
    Using `hostname --short` is not guaranteed to be POSIX, so we fall
    back to plain `hostname` and strip any domain suffix manually.
    """
    raw = (
        subprocess.check_output(["hostname"], text=True, encoding="utf-8")
        .strip()
    )
    return raw.split(".")[0]  # first label = short hostname


def test_short_hostname_resolves_to_an_ipv4():
    """
    Ensure that the machine's own short hostname can be resolved to an
    IPv4 address.  The specific IP can vary (e.g., 127.0.1.1 or a real
    interface address), so we only require that an address is returned
    and that it is a valid dotted-quad.
    """
    hostname = _get_short_hostname()

    try:
        ip = socket.gethostbyname(hostname)
    except Exception as exc:  # pragma: no cover
        pytest.fail(
            f"Name resolution failed for the current hostname {hostname!r}: {exc}"
        )

    octets = ip.split(".")
    assert len(octets) == 4 and all(
        part.isdigit() and 0 <= int(part) <= 255 for part in octets
    ), (
        f"The hostname {hostname!r} resolved to {ip!r}, which is not a valid "
        "IPv4 dotted-quad address."
    )