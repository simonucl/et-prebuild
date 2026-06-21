# test_initial_state.py
#
# This pytest suite validates the operating‐system / file-system **before**
# the student performs any action on the deployment-automation exercise.
#
# Expected initial conditions (truth value):
#   • /home/user/deploy_demo/  exists and is writable.
#   • It contains one and only one file: an **empty** README.md.
#   • No Makefile, no build/ directory, no *.log files, no other artefacts exist.
#
# NOTE: All absolute paths are hard-coded as required by the grading rules.
#       Failures are reported with clear, actionable messages.

import os
import stat
from pathlib import Path

DEPLOY_DIR = Path("/home/user/deploy_demo")
README = DEPLOY_DIR / "README.md"
MAKEFILE = DEPLOY_DIR / "Makefile"
BUILD_DIR = DEPLOY_DIR / "build"
TESTS_LOG = DEPLOY_DIR / "tests.log"
DEPLOY_LOG = DEPLOY_DIR / "deploy.log"
OUTPUT_BIN = BUILD_DIR / "output.bin"


def _dir_contents(p: Path):
    """Return sorted list of item names (str) in directory *p*, ignoring '.' and '..'."""
    return sorted(entry.name for entry in p.iterdir())


def test_deploy_demo_directory_exists():
    assert DEPLOY_DIR.exists(), f"Directory {DEPLOY_DIR} is missing."
    assert DEPLOY_DIR.is_dir(), f"{DEPLOY_DIR} exists but is not a directory."

    # Writable check: user must have write permission on the directory.
    mode = DEPLOY_DIR.stat().st_mode
    writable = bool(mode & stat.S_IWUSR)
    assert writable, f"Directory {DEPLOY_DIR} is not writable by the current user."


def test_only_empty_readme_present_initially():
    contents = _dir_contents(DEPLOY_DIR)
    assert contents == ["README.md"], (
        f"{DEPLOY_DIR} should contain only an empty README.md initially.\n"
        f"Found additional items: {[c for c in contents if c != 'README.md']}"
    )

    # README.md must exist and be empty (0 bytes).
    assert README.exists() and README.is_file(), "README.md is missing or not a regular file."
    size = README.stat().st_size
    assert size == 0, f"README.md should be empty (0 bytes) but is {size} bytes."


def test_prohibited_files_and_directories_absent():
    prohibited = [
        ("Makefile", MAKEFILE),
        ("build directory", BUILD_DIR),
        ("tests.log", TESTS_LOG),
        ("deploy.log", DEPLOY_LOG),
        ("build/output.bin", OUTPUT_BIN),
    ]

    for description, path in prohibited:
        assert not path.exists(), f"Unexpected {description} found at {path}. "