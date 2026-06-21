# test_initial_state.py
#
# Pytest suite that validates the operating-system / file-system *before*
# the student runs their solution for the “container audit” task.
#
# Truth data (what *must* already exist):
#   /home/user/images/ubuntu_latest.sif
#   /home/user/images/debian_tools.sif
#   /home/user/images/archdev.sif
#   /home/user/archive/old_centos.sif
#
# Items that must *not* yet exist:
#   /home/user/container_audit/images_snapshot_2023-10-03.log
#
# Item that may or may not exist:
#   /home/user/container_audit   (directory; the student will create it if absent)

import os
from pathlib import Path
import pytest


HOME = Path("/home/user").resolve()
EXPECTED_SIFS = {
    HOME / "images"  / "ubuntu_latest.sif",
    HOME / "images"  / "debian_tools.sif",
    HOME / "images"  / "archdev.sif",
    HOME / "archive" / "old_centos.sif",
}

AUDIT_DIR  = HOME / "container_audit"
SNAP_PATH  = AUDIT_DIR / "images_snapshot_2023-10-03.log"


def _walk_for_sifs(root: Path):
    """
    Yield every *.sif file found under ``root`` (depth-first).
    """
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".sif"):
                yield Path(dirpath) / name


def test_expected_sif_files_exist():
    """
    Every “truth” .sif file must be present *and* be a regular file.
    """
    missing = [p for p in EXPECTED_SIFS if not p.is_file()]
    assert not missing, (
        "The following expected .sif files are missing (or not regular files):\n"
        + "\n".join(map(str, missing))
    )


def test_no_unexpected_sif_files_present():
    """
    The initial system must contain *only* the four declared .sif files.
    """
    found_sifs = set(_walk_for_sifs(HOME))
    extra = sorted(map(str, found_sifs - EXPECTED_SIFS))
    missing = sorted(map(str, EXPECTED_SIFS - found_sifs))

    assert not extra and not missing, (
        "Mismatch in .sif files under /home/user.\n"
        f"Missing expected files: {missing or 'None'}\n"
        f"Unexpected extra files: {extra or 'None'}"
    )


def test_audit_directory_state():
    """
    The audit directory may or may not exist. If it *does* exist already,
    it must be a directory (not a file or symlink).
    """
    if AUDIT_DIR.exists():
        assert AUDIT_DIR.is_dir(), (
            f"{AUDIT_DIR} exists but is not a directory; "
            "remove or rename it before starting the task."
        )


def test_snapshot_file_absent_initially():
    """
    The snapshot log file must NOT exist before the student runs the task.
    """
    assert not SNAP_PATH.exists(), (
        f"The snapshot file {SNAP_PATH} already exists; "
        "it should only be created by the student's command."
    )