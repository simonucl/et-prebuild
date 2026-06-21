# test_initial_state.py
#
# This test-suite validates the **initial** state of the operating system
# *before* the student performs any deployment steps for version 1.2.3.
#
# What we are checking:
#   1. The prior release (1.2.2) is correctly laid out.
#   2. The “current” symlink points to that release **and is a symlink**.
#   3. No *other* releases are present under /home/user/app/releases/.
#
# We deliberately do **NOT** test for the files or directories that the
# student is expected to create (e.g. 1.2.3, deployment.log), as mandated
# by the grading-framework instructions.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
RELEASES_DIR = HOME / "app" / "releases"
PREV_RELEASE = RELEASES_DIR / "1.2.2"
PREV_JAR = PREV_RELEASE / "app.jar"
CURRENT_SYMLINK = HOME / "app" / "current"


def _explain_permissions(path: Path) -> str:
    """Return a human readable string of permissions and owner info (best-effort)."""
    try:
        st = path.lstat()
        mode = stat.S_IMODE(st.st_mode)
        return f"mode={oct(mode)}, uid={st.st_uid}, gid={st.st_gid}"
    except FileNotFoundError:
        return "<path does not exist>"


def test_previous_release_directory_exists_and_is_directory():
    assert PREV_RELEASE.exists(), (
        f"Expected directory {PREV_RELEASE} to exist, but it is missing."
    )
    assert PREV_RELEASE.is_dir(), (
        f"{PREV_RELEASE} exists but is not a directory "
        f"({ _explain_permissions(PREV_RELEASE) })."
    )


def test_previous_release_contains_app_jar():
    assert PREV_JAR.exists(), (
        f"Expected file {PREV_JAR} to exist inside the previous release, "
        "but it is missing."
    )
    assert PREV_JAR.is_file(), (
        f"{PREV_JAR} exists but is not a regular file."
    )
    # Basic sanity check: file is not zero-length
    size = PREV_JAR.stat().st_size
    assert size > 0, f"{PREV_JAR} is unexpectedly empty (size == 0 bytes)."


def test_current_is_a_symlink_pointing_to_previous_release():
    assert CURRENT_SYMLINK.exists(), (
        f"Expected symlink {CURRENT_SYMLINK} to exist, but it is missing."
    )
    assert CURRENT_SYMLINK.is_symlink(), (
        f"{CURRENT_SYMLINK} exists but is not a symbolic link."
    )
    target = os.readlink(CURRENT_SYMLINK)
    expected_target = str(PREV_RELEASE)
    assert target == expected_target, (
        f"{CURRENT_SYMLINK} points to '{target}' but should point to "
        f"'{expected_target}'."
    )


def test_no_other_releases_present():
    """
    There should be exactly one directory (1.2.2) under /home/user/app/releases/
    at this stage.
    """
    children = [c.name for c in RELEASES_DIR.iterdir() if c.is_dir()]
    assert children == ["1.2.2"], (
        "Unexpected directories found under "
        f"{RELEASES_DIR}: {children!r}. Only '1.2.2' should be present "
        "before deployment starts."
    )