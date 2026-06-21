# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem **before**
# the student runs any solution code.  It ensures that:
#
# 1.  /home/user/security  does NOT exist yet.
# 2.  The three expected shell-script files exist at their absolute paths.
# 3.  deploy.sh  and  cleanup.sh  are world-writable (permission bit 002 set).
# 4.  build.sh is *not* world-writable (normal 755 permissions).
# 5.  deploy.sh  and  cleanup.sh  are empty, yielding the well-known SHA-256
#    digest for an empty file.
#
# If any assertion fails, the accompanying message should tell the learner
# exactly what is missing or mis-configured.
#
# Only stdlib + pytest are used.

import os
import stat
import hashlib
from pathlib import Path

PROJECT_ROOT = Path("/home/user/my_app")
SECURITY_DIR = Path("/home/user/security")

# Absolute paths to the three scripts we expect to exist
DEPLOY_SH   = PROJECT_ROOT / "deploy.sh"
CLEANUP_SH  = PROJECT_ROOT / "scripts" / "cleanup.sh"
BUILD_SH    = PROJECT_ROOT / "scripts" / "build.sh"

EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb924"
    "27ae41e4649b934ca495991b7852b855"
)

def octal_permissions(path: Path) -> str:
    """Return the permission bits as a zero-stripped octal string (e.g. '755')."""
    mode = path.stat().st_mode & 0o777
    return f"{mode:o}"


def sha256_of_file(path: Path) -> str:
    """Compute the SHA-256 digest of the file, returned as 64 lower-hex chars."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
#  Tests
# --------------------------------------------------------------------------- #

def test_security_dir_absent_initially():
    """The security directory must *not* exist before the student runs anything."""
    assert not SECURITY_DIR.exists(), (
        f"{SECURITY_DIR} should NOT exist yet; it must be created by the student."
    )


def test_expected_script_files_exist():
    """All required script files must be present at their absolute paths."""
    for script in (DEPLOY_SH, CLEANUP_SH, BUILD_SH):
        assert script.is_file(), f"Expected file missing: {script}"


def test_world_writable_scripts_permissions():
    """deploy.sh and cleanup.sh must be world-writable (permission 777)."""
    for script in (DEPLOY_SH, CLEANUP_SH):
        perms = octal_permissions(script)
        assert perms == "777", (
            f"{script} should have permissions 777 (world-writable); "
            f"found {perms}"
        )


def test_non_world_writable_build_sh():
    """build.sh must *not* be world-writable; it should have normal 755 perms."""
    perms = octal_permissions(BUILD_SH)
    assert perms == "755", f"{BUILD_SH} should have permissions 755; found {perms}"


def test_empty_world_writable_files_have_empty_sha256():
    """deploy.sh and cleanup.sh are empty, so their SHA-256 should match that of an empty file."""
    for script in (DEPLOY_SH, CLEANUP_SH):
        digest = sha256_of_file(script)
        assert digest == EMPTY_SHA256, (
            f"{script} expected SHA-256 of empty file "
            f"({EMPTY_SHA256}); got {digest}"
        )