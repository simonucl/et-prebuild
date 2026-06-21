# test_initial_state.py
#
# Pytest suite that validates the filesystem state **before** the student
# performs any actions for the “datasets” symlink-management exercise.
#
# DO NOT MODIFY THIS FILE.
#
# The checks here enforce the exact pre-conditions described in the task:
#   • Required directories and the single broken link must already exist.
#   • *None* of the deliverables (new “active” directory, four new links,
#     replacement link in “archive”, audit log) may exist yet.
#
# Any failure tells the student (and the autograder) that the starting
# environment is incorrect, rather than the student’s solution.

import os
import stat
import pytest
from pathlib import Path

# ---------- constants ---------- #

HOME = Path("/home/user")
DATASETS = HOME / "datasets"

RAW = DATASETS / "raw"
PROCESSED = DATASETS / "processed"
ARCHIVE = DATASETS / "archive"
ACTIVE = DATASETS / "active"          # must **not** exist yet

BROKEN_LINK = ARCHIVE / "exp_old"     # must exist, but be dangling
REPLACEMENT_LINK = ARCHIVE / "exp_old_to_A"  # must **not** exist yet

RAW_EXP_A = RAW / "experiment_A"
RAW_EXP_B = RAW / "experiment_B"
PROC_EXP_A = PROCESSED / "experiment_A_clean"
PROC_EXP_B = PROCESSED / "experiment_B_clean"

AUDIT_LOG = DATASETS / "symlink_audit.log"

# The four links that will eventually live inside “active”.
ACTIVE_LINKS = {
    ACTIVE / "expA_raw",
    ACTIVE / "expB_raw",
    ACTIVE / "expA_processed",
    ACTIVE / "expB_processed",
}

# ---------- helper functions ---------- #

def _is_broken_symlink(path: Path) -> bool:
    """Return True if *path* is a symlink that does *not* resolve to
    an existing filesystem object."""
    return path.is_symlink() and not path.exists()

# ---------- tests ---------- #

def test_required_directories_present():
    """All prerequisite directories must already exist."""
    required_dirs = [
        DATASETS,
        RAW,
        RAW_EXP_A,
        RAW_EXP_B,
        PROCESSED,
        PROC_EXP_A,
        PROC_EXP_B,
        ARCHIVE,
    ]
    for d in required_dirs:
        assert d.is_dir(), f"Required directory missing: {d}"

def test_broken_link_present_and_dangling():
    """The lone pre-existing symlink must exist and be *broken*."""
    assert BROKEN_LINK.is_symlink(), (
        f"{BROKEN_LINK} should exist as a symbolic link before the exercise starts."
    )

    # Check that it is indeed broken.
    assert _is_broken_symlink(BROKEN_LINK), (
        f"{BROKEN_LINK} is expected to be a dangling/broken symlink, "
        "but it resolves to a live target."
    )

    # Verify that the link’s stored target matches the spec (“../raw/missing_experiment”).
    target_text = os.readlink(BROKEN_LINK)
    expected_target = "../raw/missing_experiment"
    assert target_text == expected_target, (
        f"{BROKEN_LINK} should point to {expected_target!r} "
        f"but instead points to {target_text!r}."
    )

def test_deliverables_absent_initially():
    """None of the files or links the student must create should exist yet."""
    # 1. The /home/user/datasets/active directory must NOT exist yet.
    assert not ACTIVE.exists(), (
        f"{ACTIVE} should NOT exist before the student runs their commands."
    )

    # 2. None of the four symlinks that will belong in 'active' may exist.
    for link_path in ACTIVE_LINKS:
        assert not link_path.exists(), (
            f"{link_path} should not exist yet (deliverable to be created by the student)."
        )
        # Even if path object is a broken symlink, .exists() would already be False,
        # but we also want to assert that the filesystem entry simply isn't there.
        assert not link_path.lstat().st_mode if link_path.exists() else True

    # 3. Replacement link in archive must NOT exist yet.
    assert not REPLACEMENT_LINK.exists(), (
        f"{REPLACEMENT_LINK} must NOT exist at the outset; the student will create it."
    )

    # 4. Audit log must NOT exist yet.
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} should not exist before the student generates it."
    )

def test_no_unexpected_symlinks_under_datasets():
    """
    Aside from the single known broken link in 'archive',
    there should be no *other* symlinks anywhere under /home/user/datasets.
    This prevents hidden state from contaminating the exercise.
    """
    unexpected_links = []

    for root, dirs, files in os.walk(DATASETS):
        for name in dirs + files:
            path = Path(root) / name
            if path.is_symlink() and path != BROKEN_LINK:
                # Any symlink other than exp_old is unexpected at this stage.
                unexpected_links.append(path)

    assert not unexpected_links, (
        "Unexpected symbolic links present before the exercise starts:\n"
        + "\n".join(str(p) for p in sorted(unexpected_links))
    )