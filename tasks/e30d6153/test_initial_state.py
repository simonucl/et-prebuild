# test_initial_state.py
#
# Pytest suite that validates the operating-system state *before* the
# learner begins the “package diagnostics” exercise.  The checks confirm
# that no residual artefacts from a previous run are present so that the
# student starts from a clean slate.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
SUPPORT_DIR = HOME / "support"
PKG_LOG = SUPPORT_DIR / "pkg_diag.log"


def _is_world_readable(file_path: Path) -> bool:
    """
    Helper that returns True iff the file is world-readable (any owner),
    i.e. the  ‘other’ read bit is set in the permission mask.
    """
    mode = file_path.stat().st_mode
    return bool(mode & stat.S_IROTH)


def test_pkg_diag_log_does_not_exist():
    """
    The diagnostic log must NOT exist yet.  A pre-existing file would
    indicate that someone has already completed (or partially completed)
    the exercise, making the initial-state check invalid.
    """
    assert not PKG_LOG.exists(), (
        f"Found unexpected file {PKG_LOG}. The exercise must start with no "
        f"pkg_diag.log present."
    )


def test_support_directory_absent_or_empty():
    """
    The directory /home/user/support should either be completely absent or
    present but empty.  The task will create the directory (if needed) and
    populate it with pkg_diag.log.  Any pre-existing content could break
    downstream grading which demands that *only* pkg_diag.log be present.
    """
    if not SUPPORT_DIR.exists():
        # Directory is absent – that is acceptable.
        return

    # If the path exists, it must be a directory.
    assert SUPPORT_DIR.is_dir(), (
        f"{SUPPORT_DIR} exists but is not a directory. Remove or rename "
        f"it so the learner can create the required directory."
    )

    # Directory must be empty.
    contents = [p.name for p in SUPPORT_DIR.iterdir()]
    assert contents == [], (
        f"{SUPPORT_DIR} is expected to be empty before the task starts, "
        f"but found: {', '.join(contents)}"
    )


def test_no_world_readable_files_preexist():
    """
    Sanity check: there should be no world-readable files lurking inside
    /home/user/support *before* the exercise.  This keeps permissions
    predictable for subsequent grading.
    """
    if not SUPPORT_DIR.exists():
        pytest.skip("Support directory does not exist – nothing to check.")

    offenders = [
        p for p in SUPPORT_DIR.iterdir()
        if p.is_file() and _is_world_readable(p)
    ]
    assert offenders == [], (
        f"Unexpected world-readable files found in {SUPPORT_DIR}: "
        f"{', '.join(str(p) for p in offenders)}. The directory should be "
        f"empty or absent at the start."
    )