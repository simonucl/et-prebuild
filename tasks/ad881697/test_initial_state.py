# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating-system /
# filesystem for the checksum-manifest exercise.
#
# The checks performed here guarantee that:
#   • The project skeleton is present exactly as described.
#   • The three placeholder files are *empty* (zero bytes).
#   • The manifest and verification-log files exist and contain the exact
#     expected bytes (including the final newline and no trailing whitespace).
#   • Running “sha256sum -c checksums.sha256” inside /home/user/project
#     succeeds with the expected output and a zero exit status.
#
# Only the Python standard library and pytest are used.

import os
import subprocess
import sys
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
BASE_DIR = Path("/home/user/project").resolve()
MANIFEST_PATH = BASE_DIR / "checksums.sha256"
LOG_PATH = BASE_DIR / "checksum_verification.log"

DIGEST_EMPTY_FILE = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

MANIFEST_CONTENT = (
    f"{DIGEST_EMPTY_FILE}  README.md\n"
    f"{DIGEST_EMPTY_FILE}  data/sample.txt\n"
    f"{DIGEST_EMPTY_FILE}  src/main.py\n"
).encode("utf-8")

LOG_CONTENT = (
    "README.md: OK\n"
    "data/sample.txt: OK\n"
    "src/main.py: OK\n"
).encode("utf-8")


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _assert_file_exists(path: Path):
    assert path.exists(), f"Expected file does not exist: {path}"
    assert path.is_file(), f"Expected a file but found something else: {path}"


def _assert_dir_exists(path: Path):
    assert path.exists(), f"Expected directory does not exist: {path}"
    assert path.is_dir(), f"Expected a directory but found something else: {path}"


def _read_bytes(path: Path) -> bytes:
    with path.open("rb") as fp:
        return fp.read()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_project_structure():
    """Verify that the directory tree and empty placeholder files exist."""
    _assert_dir_exists(BASE_DIR)

    # Directories
    _assert_dir_exists(BASE_DIR / "data")
    _assert_dir_exists(BASE_DIR / "src")

    # Files that must exist and be *empty*
    for rel_file in ("README.md", "data/sample.txt", "src/main.py"):
        file_path = BASE_DIR / rel_file
        _assert_file_exists(file_path)
        size = file_path.stat().st_size
        assert (
            size == 0
        ), f"File {file_path} should be empty (zero bytes) but has size {size}."


def test_manifest_content_is_correct():
    """The checksums.sha256 file must exist and match the exact expected bytes."""
    _assert_file_exists(MANIFEST_PATH)

    actual_bytes = _read_bytes(MANIFEST_PATH)
    assert (
        actual_bytes == MANIFEST_CONTENT
    ), (
        "The content of checksums.sha256 is incorrect.\n"
        "Expected (repr):\n"
        f"{repr(MANIFEST_CONTENT)}\n"
        "Actual (repr):\n"
        f"{repr(actual_bytes)}"
    )


def test_log_content_is_correct():
    """The checksum_verification.log file must exist and match the expected bytes."""
    _assert_file_exists(LOG_PATH)

    actual_bytes = _read_bytes(LOG_PATH)
    assert (
        actual_bytes == LOG_CONTENT
    ), (
        "The content of checksum_verification.log is incorrect.\n"
        "Expected (repr):\n"
        f"{repr(LOG_CONTENT)}\n"
        "Actual (repr):\n"
        f"{repr(actual_bytes)}"
    )


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="sha256sum is not reliably available on Windows test runners.",
)
def test_sha256sum_check_passes():
    """
    Run `sha256sum -c checksums.sha256` inside the project directory and ensure:
      • Exit status is 0.
      • STDOUT matches the expected verification log exactly.
      • STDERR is empty.
    """
    cmd = ["sha256sum", "-c", "checksums.sha256"]
    result = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,  # decode as str for easier comparison
    )

    assert (
        result.returncode == 0
    ), f"`{' '.join(cmd)}` exited with code {result.returncode}.\nSTDERR:\n{result.stderr}"

    expected_stdout = LOG_CONTENT.decode("utf-8")
    assert (
        result.stdout == expected_stdout
    ), (
        "STDOUT from sha256sum -c does not match expected verification log.\n"
        f"Expected (repr): {repr(expected_stdout)}\n"
        f"Actual (repr):   {repr(result.stdout)}"
    )

    assert (
        result.stderr == ""
    ), f"sha256sum produced unexpected STDERR output:\n{result.stderr}"