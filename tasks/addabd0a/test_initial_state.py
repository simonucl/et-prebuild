# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem / OS state
# before the student’s release-automation script is executed.
#
# The assertions follow the task description’s “CURRENT STARTING LAYOUT”.
# Any failure means the playground was not prepared correctly or the
# student tried to modify the state *before* running this test suite.

import os
from pathlib import Path

HOME = Path("/home/user").expanduser().resolve()

RELEASES_DIR = HOME / "releases"
SHARED_DIR   = RELEASES_DIR / "shared"
LEGACY_REL   = RELEASES_DIR / "release-1.0.0"
NEW_REL      = RELEASES_DIR / "release-2.0.0"          # must **not** exist yet
CURRENT_LNK  = HOME / "current"

LOGS_DIR         = HOME / "logs"
UPLOADS_DIR      = HOME / "uploads"
DEPLOY_LOGS_DIR  = HOME / "deployment_logs"
EXPECTED_DEPLOY_LOG = DEPLOY_LOGS_DIR / "deploy-release-2.0.0.log"


def test_releases_directory_structure():
    """Basic directory skeleton must already be present."""
    assert RELEASES_DIR.is_dir(), f"Expected directory {RELEASES_DIR} to exist."
    assert SHARED_DIR.is_dir(),   f"Expected shared directory {SHARED_DIR} to exist."
    assert LEGACY_REL.is_dir(),   f"Expected legacy release dir {LEGACY_REL} to exist."

def test_shared_contents_exist_and_are_files():
    """Shared dir must contain config/settings.yml, scripts/start.sh, scripts/stop.sh"""
    cfg = SHARED_DIR / "config" / "settings.yml"
    start = SHARED_DIR / "scripts" / "start.sh"
    stop  = SHARED_DIR / "scripts" / "stop.sh"

    for fp in (cfg, start, stop):
        assert fp.is_file(), f"Expected file {fp} to exist."

def test_shared_file_exact_contents():
    """Verify exact bytes of the seed files so later copy checks are deterministic."""
    cfg = (SHARED_DIR / "config" / "settings.yml").read_text(encoding="utf-8")
    start = (SHARED_DIR / "scripts" / "start.sh").read_text(encoding="utf-8")
    stop  = (SHARED_DIR / "scripts" / "stop.sh").read_text(encoding="utf-8")

    assert cfg == "staging: {}\n", \
        "Unexpected content in shared/config/settings.yml"
    assert start == "#!/bin/bash\necho starting\n", \
        "Unexpected content in shared/scripts/start.sh"
    assert stop == "#!/bin/bash\necho stopping\n", \
        "Unexpected content in shared/scripts/stop.sh"

def test_current_symlink_points_to_legacy_release():
    """/home/user/current must be a symlink that still points to release-1.0.0"""
    assert CURRENT_LNK.is_symlink(), f"{CURRENT_LNK} must be a symbolic link."
    target = os.readlink(CURRENT_LNK)             # do *not* resolve; we want the raw string
    expected = str(LEGACY_REL)
    assert target == expected, \
        f"{CURRENT_LNK} should point to {expected!r}, but points to {target!r}"

def test_auxiliary_directories_present_and_are_dirs():
    """logs/, uploads/, deployment_logs/ must exist and be directories."""
    for d in (LOGS_DIR, UPLOADS_DIR, DEPLOY_LOGS_DIR):
        assert d.is_dir(), f"Expected directory {d} to exist."
        assert not d.is_symlink(), f"{d} should be a real directory, not a symlink."

def test_no_new_release_or_deploy_log_exist_yet():
    """Before student action there must be *no* release-2.0.0 dir or deploy log."""
    assert not NEW_REL.exists(), \
        f"{NEW_REL} should NOT exist yet; it will be created by the student's script."
    assert not EXPECTED_DEPLOY_LOG.exists(), \
        f"Deployment log {EXPECTED_DEPLOY_LOG} should NOT exist yet."