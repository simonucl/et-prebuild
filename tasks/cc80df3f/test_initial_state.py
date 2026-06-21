# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# before the student carries out any actions.  It checks that:
#
# 1. /home/user/logs/ssl_error.log exists with the exact, expected
#    contents (including the trailing newline).
# 2. The auxiliary directory /home/user/cert_debug **does not yet exist**,
#    nor does its target output file.
#
# If any of these assertions fail, the test output will explain precisely
# what is missing or unexpected.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
ERROR_LOG = LOGS_DIR / "ssl_error.log"
CERT_DIR = HOME / "cert_debug"
CERT_SUMMARY = CERT_DIR / "cert_error_summary.log"

EXPECTED_LOG_LINES = [
    "[2024-02-01 10:15:20] ERROR tls: certificate verify failed for domain example.com",
    "[2024-02-01 10:20:50] ERROR tls: certificate verify failed for domain api.example.com",
    "[2024-02-01 11:00:05] ERROR tls: certificate verify failed for domain example.com",
    "[2024-02-01 11:30:00] INFO handshake succeeded for domain good.com",
    "[2024-02-01 12:45:35] ERROR tls: certificate verify failed for domain test.site",
    "[2024-02-01 13:00:00] ERROR tls: certificate verify failed for domain api.example.com",
]


def _read_text_file(path: Path) -> str:
    """Utility to read text file as UTF-8, raising a clear error if missing."""
    if not path.exists():
        pytest.fail(f"Expected file {path} to exist but it does not.")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        pytest.fail(f"Could not read file {path}: {exc!s}")


def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), f"Required directory {LOGS_DIR} is missing or is not a directory."


def test_ssl_error_log_exists_and_exact_contents():
    assert ERROR_LOG.is_file(), f"Required log file {ERROR_LOG} is missing."

    content = _read_text_file(ERROR_LOG)

    # 1. File must end with a single newline.
    assert content.endswith(
        "\n"
    ), f"File {ERROR_LOG} must end with a newline character."

    # 2. Split into lines without the trailing newline characters.
    actual_lines = content.rstrip("\n").split("\n")

    assert (
        actual_lines == EXPECTED_LOG_LINES
    ), (
        f"Contents of {ERROR_LOG} do not match the expected initial log lines.\n"
        f"Expected:\n{EXPECTED_LOG_LINES!r}\n\n"
        f"Actual:\n{actual_lines!r}"
    )


def test_cert_debug_directory_absent_initially():
    assert not CERT_DIR.exists(), (
        f"Directory {CERT_DIR} should NOT exist before the student starts; "
        "found an unexpected file or directory with that name."
    )


def test_cert_error_summary_log_absent_initially():
    assert not CERT_SUMMARY.exists(), (
        f"File {CERT_SUMMARY} should NOT exist before the student starts; "
        "found an unexpected file."
    )