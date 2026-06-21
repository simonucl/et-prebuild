# test_initial_state.py
#
# Pytest suite that validates the required *initial* state of the operating
# system / filesystem for the “performance-alert module” assignment.
#
# The tests make sure that the student has **already** created the expected
# directory structure, files, permissions and a runnable monitoring script.
#
# Only Python’s standard-library modules and pytest are used, as required.

import os
import stat
import signal
import subprocess
import time
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
MONITOR_DIR = HOME / "monitoring"

THRESHOLDS_CONF = MONITOR_DIR / "thresholds.conf"
PERF_ALERT_SH = MONITOR_DIR / "perf_alert.sh"
ALERTS_LOG = MONITOR_DIR / "alerts.log"

SAMPLE_ALERT_LINE = (
    '[2023-01-01 00:00:00] ALERT: {"metric":"cpu","value":99,"threshold":80}'
)

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #


def _is_executable(path: Path) -> bool:
    """
    Return True if *path* is executable by the current process’ user.
    """
    return os.access(path, os.X_OK)


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #


def test_monitoring_directory_exists():
    """
    The directory /home/user/monitoring **must** exist.
    """
    assert MONITOR_DIR.is_dir(), (
        "Required directory '/home/user/monitoring' is missing.\n"
        "Create it exactly as specified."
    )


def test_thresholds_conf_contents():
    """
    thresholds.conf must exist and contain exactly two expected lines.
    """
    assert THRESHOLDS_CONF.is_file(), (
        "Missing file: /home/user/monitoring/thresholds.conf"
    )

    with THRESHOLDS_CONF.open() as fp:
        lines = [ln.rstrip("\n") for ln in fp.readlines()]

    assert lines == [
        "CPU_THRESHOLD=80",
        "MEM_THRESHOLD=70",
    ], (
        "File /home/user/monitoring/thresholds.conf must contain **exactly**:\n"
        "CPU_THRESHOLD=80\nMEM_THRESHOLD=70\n"
        f"Current contents were:\n{lines!r}"
    )


def test_perf_alert_sh_is_executable_and_has_shebang():
    """
    perf_alert.sh must exist, be executable, and start with '#!/bin/bash'.
    """
    assert PERF_ALERT_SH.is_file(), (
        "Missing file: /home/user/monitoring/perf_alert.sh"
    )

    # Check the shebang on the first line
    with PERF_ALERT_SH.open("r", encoding="utf-8", errors="replace") as fp:
        first_line = fp.readline().rstrip("\n")

    assert (
        first_line == "#!/bin/bash"
    ), "First line of perf_alert.sh must be exactly '#!/bin/bash'"

    # Check the executable bit
    assert _is_executable(
        PERF_ALERT_SH
    ), "perf_alert.sh exists but is **not** marked as executable (chmod +x missing)"


def test_alerts_log_contains_sample_line():
    """
    alerts.log must exist and include the required deterministic sample alert line.
    """
    assert ALERTS_LOG.is_file(), (
        "Missing file: /home/user/monitoring/alerts.log"
    )

    with ALERTS_LOG.open("r", encoding="utf-8", errors="replace") as fp:
        contents = fp.read().splitlines()

    assert (
        SAMPLE_ALERT_LINE in contents
    ), (
        "alerts.log does not contain the required sample alert line:\n"
        f"{SAMPLE_ALERT_LINE}\n"
        "Make sure you appended it verbatim."
    )


@pytest.mark.timeout(10)
def test_perf_alert_runs_for_at_least_two_seconds():
    """
    Launch perf_alert.sh and verify that it stays alive for at least two seconds
    (indicating that it parsed thresholds.conf and began sampling). Then send
    SIGINT to stop it gracefully.
    """
    assert _is_executable(
        PERF_ALERT_SH
    ), "perf_alert.sh is not executable, cannot be launched for runtime test"

    # Start the script via bash to avoid relying on the shebang path resolution
    proc = subprocess.Popen(
        ["bash", str(PERF_ALERT_SH)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give the script 2 seconds to prove it stays up
        time.sleep(2)

        # If the process has already exited, capture its output and fail
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            pytest.fail(
                "perf_alert.sh exited prematurely (within 2 seconds).\n"
                f"stdout:\n{stdout}\n\nstderr:\n{stderr}"
            )

        # Ask it to terminate (Ctrl-C behaviour)
        proc.send_signal(signal.SIGINT)

        # Wait a reasonable amount of time for clean shutdown
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force-kill as a last resort to avoid hanging the test suite
            proc.kill()
            stdout, stderr = proc.communicate()
            pytest.fail(
                "perf_alert.sh did not terminate after SIGINT.\n"
                f"stdout:\n{stdout}\n\nstderr:\n{stderr}"
            )
    finally:
        # Ensure child processes are not left behind
        if proc.poll() is None:
            proc.kill()