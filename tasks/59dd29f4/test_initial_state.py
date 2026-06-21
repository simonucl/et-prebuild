# test_initial_state.py
#
# This pytest suite verifies the *initial* workstation state
# before the student executes any command.  It confirms that:
#
# 1. The directory /home/user/images exists.
# 2. Exactly three *.sif files are present inside it:
#       ubuntu_latest.sif
#       alpine_3.18.sif
#       node_18.sif
#    They must be regular files (not symlinks or directories).
# 3. No other *.sif files are present in /home/user/images.
# 4. The file /home/user/container_list.md must NOT exist yet.
#
# If any of these conditions are unmet, the test will fail with a
# clear, actionable message.

from pathlib import Path
import os
import stat
import pytest

HOME = Path("/home/user")
IMAGES_DIR = HOME / "images"
EXPECTED_IMAGES = {
    "ubuntu_latest.sif",
    "alpine_3.18.sif",
    "node_18.sif",
}
CONTAINER_LIST_MD = HOME / "container_list.md"


def is_regular_file(path: Path) -> bool:
    """
    Return True if path is an existing *regular* file (not dir, not symlink).
    """
    try:
        st_mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(st_mode)


def test_images_directory_exists_and_is_dir():
    assert IMAGES_DIR.exists(), f"Required directory {IMAGES_DIR} does not exist."
    assert IMAGES_DIR.is_dir(), f"{IMAGES_DIR} exists but is not a directory."


def test_expected_sif_files_present_and_regular():
    missing = [name for name in EXPECTED_IMAGES if not (IMAGES_DIR / name).exists()]
    assert not missing, (
        "The following expected .sif files are missing from "
        f"{IMAGES_DIR}: {', '.join(missing)}"
    )

    non_regular = [
        name
        for name in EXPECTED_IMAGES
        if not is_regular_file(IMAGES_DIR / name)
    ]
    assert not non_regular, (
        "The following expected .sif paths exist but are not regular files: "
        f"{', '.join(non_regular)}"
    )


def test_no_extra_sif_files_present():
    all_sif_files = {p.name for p in IMAGES_DIR.glob("*.sif")}
    extra = all_sif_files - EXPECTED_IMAGES
    assert not extra, (
        "Unexpected .sif files found in "
        f"{IMAGES_DIR}: {', '.join(sorted(extra))}. "
        "Only the following should be present initially: "
        f"{', '.join(sorted(EXPECTED_IMAGES))}"
    )


def test_container_list_md_absent_initially():
    assert not CONTAINER_LIST_MD.exists(), (
        f"The file {CONTAINER_LIST_MD} should NOT exist before the task is begun."
    )