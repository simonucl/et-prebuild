# test_initial_state.py
#
# This pytest suite validates that the machine is in a *clean* state
# prior to the learner creating any audit-trail artefacts for the
# “2023-Q4-Network-Diagnostics” exercise.  In particular, we assert that:
#
#   1. The target directory /home/user/audit_trails/2023-Q4-Network-Diagnostics
#      does NOT yet exist.
#   2. Consequently, none of the three required artefact files
#      (raw_log.txt, summary.json, integrity.sha256) exist either.
#
# If any of these paths already exist, the test suite will fail with a
# descriptive message so that the learner knows to start from a clean
# environment.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants – the paths that *must not* exist before the student begins.
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/audit_trails/2023-Q4-Network-Diagnostics")
REQUIRED_FILES = [
    BASE_DIR / "raw_log.txt",
    BASE_DIR / "summary.json",
    BASE_DIR / "integrity.sha256",
]


# ---------------------------------------------------------------------------
# Helper / assertion utilities
# ---------------------------------------------------------------------------

def _human_readable(mode_int: int) -> str:
    """Return a string such as '0755' from a stat().st_mode integer."""
    return oct(mode_int & 0o777)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_target_directory_absent():
    """
    The audit directory must NOT exist yet.  A pre-existing directory is a
    breach of the “start from scratch” requirement and could mask problems
    with permissions or stale files.
    """
    assert not BASE_DIR.exists(), (
        f"Pre-condition failure: directory {BASE_DIR} already exists. "
        "Please remove it before running the exercise so the audit bot can "
        "verify your freshly-created artefacts."
    )


@pytest.mark.parametrize("path", REQUIRED_FILES)
def test_artifact_files_absent(path: Path):
    """
    None of the required artefact files should exist before the student
    performs the exercise.  Existing files would prevent a clean audit trail
    and may carry incorrect data or permissions.
    """
    assert not path.exists(), (
        f"Pre-condition failure: unexpected file {path} already exists. "
        "Delete it (and its parent directory, if necessary) before starting "
        "the exercise."
    )


def test_parent_directory_permissions_if_exists():
    """
    If *any* part of /home/user/audit_trails already exists,
    its permissions must not be overly restrictive because the learner
    will need to create subdirectories within it.

    This test is *non-blocking* (xfail) – it warns but does not fail
    the suite.  It will only be relevant in edge cases where earlier
    coursework left behind a restrictive directory.
    """
    parent = BASE_DIR.parent  # /home/user/audit_trails
    if not parent.exists():
        pytest.skip(f"{parent} does not yet exist – no permission checks needed.")

    mode = parent.stat().st_mode
    readable_by_others = bool(mode & 0o004)
    writable_by_user   = bool(mode & 0o200)

    if not (readable_by_others and writable_by_user):
        pytest.xfail(
            f"Directory {parent} has permissions {_human_readable(mode)} – "
            "it should be at least readable by others (o+r) and writable by "
            "you (u+w) so that the exercise can create subdirectories."
        )