# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem state
before the student begins working on the Makefile task.

The checks are intentionally strict so that any divergence from the expected
starting snapshot is reported with a clear, human-readable error message.

Assumptions
-----------
• All work must happen in /home/user/release
• Only stdlib + pytest are available.
"""

from pathlib import Path
import gzip
import pytest

RELEASE_DIR = Path("/home/user/release").resolve()
VERSION_FILE = RELEASE_DIR / "VERSION"
APP_DIR = RELEASE_DIR / "app"
APP_MAIN = APP_DIR / "main.py"
MAKEFILE = RELEASE_DIR / "Makefile"
BUILD_DIR = RELEASE_DIR / "build"
EXPECTED_VERSION_CONTENT = "1.0.0\n"


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path}: {exc}")


def test_release_directory_exists():
    assert RELEASE_DIR.exists(), (
        f"Directory {RELEASE_DIR} is missing; the initial workspace "
        "must already exist."
    )
    assert RELEASE_DIR.is_dir(), f"{RELEASE_DIR} exists but is not a directory."


def test_version_file_present_and_correct():
    assert VERSION_FILE.exists(), f"Expected VERSION file at {VERSION_FILE} is missing."
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} exists but is not a file."
    content = _read_text(VERSION_FILE)
    assert (
        content == EXPECTED_VERSION_CONTENT
    ), (
        f"VERSION file should contain exactly {EXPECTED_VERSION_CONTENT!r} "
        f"but found {content!r}."
    )


def test_app_directory_and_main_py_present():
    assert APP_DIR.exists(), f"Application directory {APP_DIR} is missing."
    assert APP_DIR.is_dir(), f"{APP_DIR} exists but is not a directory."
    assert APP_MAIN.exists(), f"Expected file {APP_MAIN} is missing."
    assert APP_MAIN.is_file(), f"{APP_MAIN} exists but is not a file."
    # We don't mandate exact content, but ensure it's non-empty for sanity.
    source = _read_text(APP_MAIN)
    assert source.strip(), f"{APP_MAIN} appears to be empty."


def test_makefile_does_not_yet_exist():
    assert not MAKEFILE.exists(), (
        f"Makefile {MAKEFILE} already exists, but the initial state should "
        "NOT contain it. The student is supposed to create this file."
    )


def test_build_artifacts_absent():
    assert not BUILD_DIR.exists(), (
        f"Build directory {BUILD_DIR} is present, but should NOT exist in the "
        "initial state."
    )
    # Also ensure no stray tarballs are present
    tarballs = list(RELEASE_DIR.glob("build/app-*.tar.gz"))
    assert not tarballs, (
        f"Found unexpected tarballs in {RELEASE_DIR / 'build'}: {tarballs}. "
        "The build output should not exist yet."
    )