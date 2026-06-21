# test_initial_state.py
"""
Pytest suite that validates the ORIGINAL filesystem state *before*
the student creates /home/user/release and its contents.

The tests assert that the supplied “project” directory already exists
and that **none** of the required deliverables inside /home/user/release
have been created yet.

If any assertion fails, it means the exercise is starting from an
unexpected state and the student’s work cannot be assessed reliably.
"""

import os
from pathlib import Path

# ---------- Constants --------------------------------------------------------

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
PROJECT_SRC_DIR = PROJECT_DIR / "src"
APP_FILE = PROJECT_SRC_DIR / "app.py"

RELEASE_DIR = HOME / "release"
PREPARE_SCRIPT = RELEASE_DIR / "prepare_release.sh"
VERSION_FILE = RELEASE_DIR / "version.txt"
RELEASE_LOG = RELEASE_DIR / "releases.log"


# ---------- Helper -----------------------------------------------------------

def _read_file(path: Path) -> str:
    """Return file contents as str; fail clearly if file missing."""
    assert path.exists(), f"Expected file to exist: {path}"
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# ---------- Tests ------------------------------------------------------------

def test_project_structure_exists():
    """
    Ensure the seed “project” directory is present and correctly populated.
    """
    assert PROJECT_DIR.is_dir(), f"Missing directory: {PROJECT_DIR}"
    assert PROJECT_SRC_DIR.is_dir(), f"Missing directory: {PROJECT_SRC_DIR}"
    assert APP_FILE.is_file(), f"Missing file: {APP_FILE}"

    expected_content = (
        "# sample source file\n"
        'print("Hello from project")\n'
    )
    actual_content = _read_file(APP_FILE)
    assert actual_content == expected_content, (
        f"Unexpected contents in {APP_FILE}.\n"
        "Expected:\n"
        f"{expected_content!r}\n"
        "Got:\n"
        f"{actual_content!r}"
    )


def test_release_artifacts_do_not_exist_yet():
    """
    Verify that nothing related to /home/user/release exists yet.
    The student will create these during the exercise.
    """
    assert not RELEASE_DIR.exists(), (
        f"{RELEASE_DIR} should NOT exist before the student runs the task."
    )

    # Even if the directory does exist (e.g. due to prior runs),
    # confirm that no deliverable files are already present.
    for path in (PREPARE_SCRIPT, VERSION_FILE, RELEASE_LOG):
        assert not path.exists(), (
            f"{path} should NOT exist at the beginning of the task."
        )