# test_initial_state.py
#
# These tests validate the *initial* state of the operating system before the
# student starts working on the “firewall snapshot” task.  Nothing that the
# student is supposed to create should exist yet, while the required system
# commands must already be available.
#
# If any of the required artefacts are already present, the tests will fail
# with a clear, actionable message so that the environment can be reset.

import shutil
import subprocess
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
FW_DIR = Path("/home/user/fw_diagnostics")

REQUIRED_FILES = {
    "iptables_list": FW_DIR / "iptables_list.txt",
    "iptables_rules": FW_DIR / "iptables_rules.txt",
    "listening_ports": FW_DIR / "listening_ports.txt",
}

ARCHIVE = FW_DIR / "fw_snapshot.tar.gz"


def _cmd_available(cmd: str) -> bool:
    """
    Returns True if *cmd* can be found in the user's PATH **and** can be
    executed (using `--version` which does not require privileges).
    """
    exe = shutil.which(cmd)
    if exe is None:
        return False

    try:
        # Use --version because it is guaranteed to be harmless and quick.
        subprocess.run(
            [exe, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except Exception:
        return False
    return True


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_required_commands_present():
    """
    The student will need to run exactly three commands:
        * iptables -L -n -v
        * iptables -S
        * ss -lnptu

    We verify that the corresponding executables (`iptables` and `ss`) are
    available and callable without super-user privileges so that the task is
    actually solvable.
    """
    missing = [cmd for cmd in ("iptables", "ss") if not _cmd_available(cmd)]
    assert not missing, (
        "The following required command(s) are not available or not callable: "
        f"{', '.join(missing)}"
    )


def test_snapshot_files_do_not_exist_yet():
    """
    None of the artefacts that the student has to create should exist before
    they start working on the task.
    """
    pre_existing = [p for p in REQUIRED_FILES.values() if p.exists()]
    assert (
        not pre_existing
    ), "The following snapshot file(s) already exist but should not:\n" + "\n".join(
        str(p) for p in pre_existing
    )


def test_archive_does_not_exist_yet():
    """
    The final tar.gz archive must not exist before the student has created it.
    """
    assert not ARCHIVE.exists(), (
        "Archive {0} already exists but the student has not yet run their "
        "solution.  Please remove it before grading.".format(ARCHIVE)
    )