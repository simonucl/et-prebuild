# test_initial_state.py
#
# Pytest suite that verifies the **initial** on–disk state for the
# “INC123” incident handling task _before_ the student performs any
# actions.  The checks enforce that the raw input data, supporting
# directories and the *absence* of deliverable artefacts all match the
# specification given in the assignment.
#
# NOTE:  If any of these tests fail, the environment your solution
# depends on is not as expected and you should re-create / fix the
# files or directories mentioned in the failure message before
# starting the actual task.

import os
import stat
from pathlib import Path

RAW_DIR = Path("/home/user/incidents/raw/INC123")
ARCHIVES_DIR = Path("/home/user/archives")
TRIAGE_DIR = Path("/home/user/incidents/triage")

# Raw file paths
APP_LOG   = RAW_DIR / "app.log"
ERR_LOG   = RAW_DIR / "error.log"
TMP_FILE  = RAW_DIR / "debug.tmp"

# Future deliverables that must NOT exist yet
TAR_FILE        = ARCHIVES_DIR / "INC123_logs.tar.gz"
MANIFEST_FILE   = ARCHIVES_DIR / "INC123_manifest.log"
TRIAGE_ERR_LOG  = TRIAGE_DIR / "error.log"
CHECKSUM_FILE   = TRIAGE_DIR / "INC123_checksum.sha256"

# Expected exact byte contents of the three raw files
APP_LOG_CONTENT = (
    "2023-11-12 10:00:00 INFO Application started\n"
    "2023-11-12 10:05:00 INFO Application stopped\n"
).encode("utf-8")

ERR_LOG_CONTENT = (
    # 58 bytes including the trailing LF
    "2023-11-12 10:03:00 ERROR NullPointerExceptio encountered\n"
).encode("utf-8")

DEBUG_TMP_CONTENT = b"temporary file to be excluded\n"


def _assert_regular_readable(p: Path):
    msg = f"Required file “{p}” is missing."
    assert p.exists(), msg
    assert p.is_file(), f"Path “{p}” exists but is not a regular file."
    mode = p.stat().st_mode
    assert stat.S_IMODE(mode) & stat.S_IRUSR, f"File “{p}” is not readable."


def _assert_directory(p: Path):
    msg = f"Required directory “{p}” is missing."
    assert p.exists(), msg
    assert p.is_dir(), f"Path “{p}” exists but is not a directory."


# ----------------------------------------------------------------------
# Directory structure checks
# ----------------------------------------------------------------------
def test_required_directories_exist():
    _assert_directory(RAW_DIR)
    _assert_directory(ARCHIVES_DIR)
    _assert_directory(TRIAGE_DIR)


# ----------------------------------------------------------------------
# Raw file presence & exclusivity
# ----------------------------------------------------------------------
def test_raw_directory_contains_exactly_expected_files():
    expected = {"app.log", "error.log", "debug.tmp"}
    actual = {p.name for p in RAW_DIR.iterdir() if p.is_file()}
    assert expected <= actual, (
        "The raw incident directory is missing one or more required files: "
        f"{expected - actual}"
    )
    # It is acceptable for extra diagnostic files to be present,
    # but *.tmp files other than debug.tmp must not exist.
    unexpected_tmp = {name for name in actual - expected if name.endswith(".tmp")}
    assert not unexpected_tmp, (
        "Unexpected “*.tmp” files found in raw directory: "
        f"{sorted(unexpected_tmp)}"
    )


# ----------------------------------------------------------------------
# Content & size verification
# ----------------------------------------------------------------------
def test_app_log_content_and_size():
    _assert_regular_readable(APP_LOG)
    data = APP_LOG.read_bytes()
    assert data == APP_LOG_CONTENT, (
        f"Content of {APP_LOG} does not match the expected 2-line log."
    )
    assert len(data) == 90, f"{APP_LOG} should be 90 bytes, found {len(data)}."


def test_error_log_content_and_size():
    _assert_regular_readable(ERR_LOG)
    data = ERR_LOG.read_bytes()
    assert data == ERR_LOG_CONTENT, (
        f"Content of {ERR_LOG} does not match the expected 1-line log."
    )
    assert len(data) == 58, f"{ERR_LOG} should be 58 bytes, found {len(data)}."


def test_debug_tmp_content_and_size():
    _assert_regular_readable(TMP_FILE)
    data = TMP_FILE.read_bytes()
    assert data == DEBUG_TMP_CONTENT, (
        f"Content of {TMP_FILE} does not match the expected string."
    )
    assert len(data) == 30, f"{TMP_FILE} should be 30 bytes, found {len(data)}."


# ----------------------------------------------------------------------
# Absence of deliverable artefacts
# ----------------------------------------------------------------------
def test_deliverable_files_do_not_exist_yet():
    for path in (TAR_FILE, MANIFEST_FILE, TRIAGE_ERR_LOG, CHECKSUM_FILE):
        assert not path.exists(), (
            f"Deliverable artefact “{path}” already exists. "
            "The workspace must start clean."
        )