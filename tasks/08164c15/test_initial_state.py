# test_initial_state.py
#
# This pytest suite verifies that the legacy monitoring utility’s **initial**
# filesystem and executable requirements are present **before** students begin
# implementing their solution.  Nothing in here checks for, or depends on, any
# files the student will create (e.g. /home/user/reports/uptime_summary.csv).

import os
import subprocess
from pathlib import Path

LEGACY_DIR = Path("/home/user/legacy_tools")
HOSTS_FILE = LEGACY_DIR / "hosts.lst"
SCRIPT_FILE = LEGACY_DIR / "run_checks.sh"


def test_legacy_directory_exists():
    assert LEGACY_DIR.is_dir(), (
        f"Required directory {LEGACY_DIR} is missing or is not a directory."
    )


def test_hosts_file_exists_and_contents():
    assert HOSTS_FILE.is_file(), (
        f"Required host list {HOSTS_FILE} does not exist or is not a regular file."
    )

    contents = HOSTS_FILE.read_text(encoding="utf-8").splitlines()
    expected = ["127.0.0.1", "localhost", "blackhole.local"]

    assert contents == expected, (
        f"{HOSTS_FILE} must contain exactly the following lines (in order): "
        f"{expected!r}. Found: {contents!r}"
    )


def test_run_checks_is_executable():
    assert SCRIPT_FILE.is_file(), (
        f"Required script {SCRIPT_FILE} does not exist or is not a regular file."
    )
    assert os.access(SCRIPT_FILE, os.X_OK), (
        f"Script {SCRIPT_FILE} exists but is not marked executable (missing +x)."
    )


def _run_script(host: str):
    """Helper: invoke run_checks.sh safely and return (exit_code, stdout_text)."""
    completed = subprocess.run(
        [str(SCRIPT_FILE), host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def test_run_checks_behavior():
    """
    The vintage script is deterministic; verify it produces the expected
    exit codes and text for each of the three canonical hosts.
    """
    scenarios = {
        "127.0.0.1": (0, "STATUS:UP LATENCY_MS:1"),
        "localhost": (0, "STATUS:UP LATENCY_MS:2"),
        "blackhole.local": (2, "STATUS:DOWN"),
    }

    for host, (expected_rc, expected_stdout) in scenarios.items():
        rc, out, err = _run_script(host)
        assert rc == expected_rc, (
            f"{SCRIPT_FILE} returned exit code {rc} for host {host!r}; "
            f"expected {expected_rc}. STDERR was: {err!r}"
        )
        assert out == expected_stdout, (
            f"{SCRIPT_FILE} output {out!r} for host {host!r}; "
            f"expected {expected_stdout!r}"
        )