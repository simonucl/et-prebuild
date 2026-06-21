# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system state for the
# “loopback ping log” exercise.  These tests run *before* the student performs
# any action, therefore they deliberately avoid checking for the existence (or
# absence) of any output artefacts such as
# `/home/user/network_logs/loopback_ping.log`.
#
# The goal is simply to make sure the host can issue ICMP echo-requests to
# 127.0.0.1, that the required `ping` utility is available, and that the
# loopback interface behaves as expected (4 packets transmitted, 4 packets
# received, 0 % packet loss).

import re
import shutil
import subprocess
import sys

import pytest


PING_COUNT = 4
LOOPBACK_ADDRESS = "127.0.0.1"


def _parse_ping_summary(stdout: str):
    """
    Extract the three key statistics from a ping summary line.

    The function supports the most common GNU, BusyBox and BSD‐style outputs,
    which typically look like one of the following:

        4 packets transmitted, 4 received, 0% packet loss, time 3063ms
        4 packets transmitted, 4 packets received, 0.0% packet loss
        4 packets transmitted, 4 packets received, 0% packet loss, time 3ms

    It returns a tuple: (tx:int, rx:int, loss:float).
    """
    # Use DOTALL so `.*?` can span newlines if necessary.
    regex = re.compile(
        r"(?P<tx>\d+)\s+packets transmitted,?\s+"
        r"(?P<rx>\d+)\s+(?:packets\s+)?received,?\s+"
        r"(?P<loss>\d+(?:\.\d+)?)%\s*packet loss",
        flags=re.IGNORECASE | re.DOTALL,
    )

    match = regex.search(stdout)
    if not match:
        raise ValueError(
            "Unable to parse ping statistics from the following output:\n"
            f"{stdout}"
        )

    return (
        int(match.group("tx")),
        int(match.group("rx")),
        float(match.group("loss")),
    )


def _run_ping(count: int, address: str, timeout: int = 10) -> str:
    """
    Execute the system `ping` command and return its full stdout as text.
    """
    ping_exe = shutil.which("ping")
    if not ping_exe:
        pytest.fail(
            "The `ping` executable could not be found in $PATH. "
            "Please ensure the system has a functional `ping` utility."
        )

    try:
        result = subprocess.run(
            [ping_exe, "-c", str(count), address],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,  # We'll examine returncode ourselves for clarity.
        )
    except FileNotFoundError:
        pytest.fail(
            f"Expected to find an executable `ping` at {ping_exe!s}, "
            "but the file is missing."
        )

    if result.returncode != 0:
        pytest.fail(
            "The `ping` command exited with a non-zero status "
            f"({result.returncode}). Output was:\n{result.stdout}"
        )

    return result.stdout


def test_ping_executable_is_available():
    """
    Ensure the `ping` utility is present and executable.
    """
    ping_path = shutil.which("ping")
    assert ping_path, (
        "No `ping` executable was found in the current PATH. "
        "The exercise requires a functioning `ping` command."
    )


def test_loopback_ping_is_healthy():
    """
    Confirm that sending 4 ICMP echo-requests to 127.0.0.1 succeeds with
    zero packet loss, indicating a healthy loopback interface.
    """
    stdout = _run_ping(PING_COUNT, LOOPBACK_ADDRESS)
    tx, rx, loss = _parse_ping_summary(stdout)

    assert (
        tx == PING_COUNT
    ), f"Expected {PING_COUNT} packets transmitted, got {tx}. Full output:\n{stdout}"
    assert (
        rx == PING_COUNT
    ), f"Expected {PING_COUNT} packets received, got {rx}. Full output:\n{stdout}"
    assert (
        loss == 0.0
    ), f"Expected 0% packet loss, got {loss}%. Full output:\n{stdout}"