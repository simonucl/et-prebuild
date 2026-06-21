# test_initial_state.py
#
# Pytest suite that validates the machine *before* the student’s solution
# is applied.  It checks the presence and integrity of the original
# ISO-8859-1 log file but deliberately avoids touching any of the files
# or directories that are supposed to be created by the student.
#
# Rules respected:
# • Only stdlib + pytest are used.
# • Full paths (/home/user/…) are tested.
# • No assertions about any output artefacts (e.g. session_utf8.log,
#   /home/user/analysis/) are made here.

from pathlib import Path
import pytest

LOGS_DIR = Path("/home/user/logs")
ISO_LOG  = LOGS_DIR / "session_iso8859.log"

EXPECTED_LINES = [
    "2023-05-01 12:00:00 INFO  User São logged in",
    "2023-05-01 12:02:13 ERROR Failed to load Balcón image",
    "2023-05-01 12:03:45 WARN  Disk almost full",
    "2023-05-01 12:05:10 ERROR Señor account locked",
    "2023-05-01 12:07:55 ERROR Timeout on payment gateway",
]


def _read_bytes(path: Path) -> bytes:
    """Utility: read file as raw bytes."""
    with path.open("rb") as f:
        return f.read()


def test_logs_directory_exists():
    """The /home/user/logs directory must already exist."""
    assert LOGS_DIR.exists(), f"Directory {LOGS_DIR} is missing."
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."


def test_iso_log_file_exists():
    """The original ISO-8859-1 session log file must be present."""
    assert ISO_LOG.exists(), f"Expected log file {ISO_LOG} is missing."
    assert ISO_LOG.is_file(), f"{ISO_LOG} exists but is not a regular file."


def test_iso_log_file_encoding_and_content():
    """
    Validate that the file:
      • Contains exactly the five expected lines (LF-terminated).
      • Is encoded in ISO-8859-1 (Latin-1) and *not* valid UTF-8.
      • Uses LF line endings only (no CR characters).
    """
    raw = _read_bytes(ISO_LOG)

    # 1. Ensure there are *no* CR characters (Windows line endings).
    assert b"\r" not in raw, (
        f"{ISO_LOG} should use LF line endings only, "
        "but CR (\\r) bytes were found."
    )

    # 2. File must end with a single LF so that every line is terminated.
    assert raw.endswith(b"\n"), (
        f"{ISO_LOG} must end with a single LF so every line is terminated."
    )

    # 3. ISO-8859-1 decoding must succeed and match the expected text.
    try:
        text_latin1 = raw.decode("latin-1")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{ISO_LOG} could not be decoded as ISO-8859-1: {exc}")

    lines = text_latin1.split("\n")[:-1]  # Drop the final empty element.
    assert lines == EXPECTED_LINES, (
        f"Content mismatch in {ISO_LOG}.\n"
        f"Expected lines:\n{EXPECTED_LINES!r}\n\n"
        f"Found lines:\n{lines!r}"
    )

    # 4. Attempting to decode as UTF-8 *must* raise an error, proving
    #    the file is not already UTF-8.
    with pytest.raises(UnicodeDecodeError):
        raw.decode("utf-8")