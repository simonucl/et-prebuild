# test_initial_state.py
#
# Pytest suite that validates the starting conditions for the
# credential-rotation exercise.  It checks only the items that must
# already exist before the student performs any action.
#
# Rules respected:
#   • Uses only stdlib + pytest
#   • Verifies absolute paths
#   • Does NOT touch or mention any output files (/home/user/rotate/new_creds.csv,
#     /home/user/rotate/rotation.log, etc.)

import pathlib
import textwrap
import pytest

# Absolute paths used throughout the checks
ROTATE_DIR = pathlib.Path("/home/user/rotate")
OLD_CREDS_FILE = ROTATE_DIR / "old_creds.csv"

# Expected exact content of /home/user/rotate/old_creds.csv, including the
# trailing newline on the final line.
EXPECTED_OLD_CREDS_CONTENT = (
    "username,password,expiration\n"
    "alice,pa55w0rd!,2023-03-01\n"
    "bob,letMeIn123,2023-04-15\n"
    "carol,S3cur3Key#,2023-05-30\n"
)


def _read_file(path: pathlib.Path) -> str:
    """
    Return the file’s text as a single string.
    The helper exists mainly to centralise the encoding choice and
    raise a clear error should the file be unreadable.
    """
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        # Re-raise with additional context but preserve the original traceback
        raise RuntimeError(f"Unable to read {path!s}: {exc}") from exc


def test_rotate_directory_exists():
    """
    Verify that /home/user/rotate exists and is a directory.
    """
    assert ROTATE_DIR.exists(), (
        f"Required directory not found: {ROTATE_DIR}\n"
        "Create the directory and place the supplied CSV inside it."
    )
    assert ROTATE_DIR.is_dir(), (
        f"Expected {ROTATE_DIR} to be a directory but it is not.\n"
        "Ensure that /home/user/rotate is created as a directory."
    )


def test_old_creds_file_exists():
    """
    Verify that /home/user/rotate/old_creds.csv exists and is a regular file.
    """
    assert OLD_CREDS_FILE.exists(), (
        f"Required file missing: {OLD_CREDS_FILE}\n"
        "Make sure the original credentials CSV is pre-populated exactly as provided."
    )
    assert OLD_CREDS_FILE.is_file(), (
        f"{OLD_CREDS_FILE} exists but is not a regular file."
    )


def test_old_creds_file_content_exact():
    """
    Ensure that the contents of old_creds.csv match the reference data
    byte-for-byte (UTF-8 encoded text comparison).
    """
    actual_content = _read_file(OLD_CREDS_FILE)

    # Fast path: exact match
    if actual_content == EXPECTED_OLD_CREDS_CONTENT:
        return

    # Detailed failure report
    diff_lines = [
        "Mismatch detected in /home/user/rotate/old_creds.csv",
        "",
        "EXPECTED:",
        *textwrap.indent(EXPECTED_OLD_CREDS_CONTENT, "    ").splitlines(),
        "",
        "ACTUAL:",
        *textwrap.indent(actual_content, "    ").splitlines(),
        "",
        "Ensure the file matches exactly, including header spelling, "
        "line order, and the single trailing newline."
    ]
    pytest.fail("\n".join(diff_lines))