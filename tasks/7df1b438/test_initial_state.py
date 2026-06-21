# test_initial_state.py
"""
Pytest suite verifying the OS / filesystem **before** the student starts working
on the “network-diagnostics” exercise.

The student is expected to create files and directories under
/home/user/netdiag.  At the beginning of the exercise none of those artefacts
must exist; otherwise a previous run (or a mis-configured image) could influence
the result.

If any of the assertions below fail, the container is in an unexpected state and
the student should *not* start working until the problems are resolved.
"""

import os
import shutil
from pathlib import Path

ROOT = Path("/home/user")
NETDIAG_DIR = ROOT / "netdiag"
RAW_DIR = NETDIAG_DIR / "raw"
CSV_FILE = NETDIAG_DIR / "network_probe_results.csv"
LOG_LOCALHOST = RAW_DIR / "127.0.0.1.log"
LOG_TESTNET = RAW_DIR / "203.0.113.1.log"


def _fmt_missing(path: Path) -> str:
    "Return a human-readable message for an unexpected path."
    if path.is_dir():
        kind = "directory"
    elif path.is_file():
        kind = "file"
    else:
        kind = "path"
    return f"Unexpected {kind} present at {path}. The workspace must start clean."


def test_clean_workspace():
    """
    No artefacts from the task should exist yet.
    """
    # The main output directory must NOT exist.
    assert not NETDIAG_DIR.exists(), _fmt_missing(NETDIAG_DIR)

    # Output CSV must NOT exist.
    assert not CSV_FILE.exists(), _fmt_missing(CSV_FILE)

    # Raw directory and its log files must NOT exist.
    for path in (RAW_DIR, LOG_LOCALHOST, LOG_TESTNET):
        assert not path.exists(), _fmt_missing(path)


def test_ping_available():
    """
    The unprivileged `ping` binary must be available in PATH so the student can
    perform ICMP probes without installing additional software.
    """
    ping_path = shutil.which("ping")
    assert ping_path is not None, (
        "The `ping` command is not available in the container's PATH. "
        "It is required for the exercise."
    )
    assert Path(ping_path).is_file(), (
        f"`ping` binary was expected at {ping_path}, but the path is not a file."
    )