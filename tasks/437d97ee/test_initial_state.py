# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the container **before**
# the student’s solution runs.  It checks that the seed configuration file and
# directory layout match the specification and that none of the artefacts the
# student is supposed to create are present yet.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
CFG_DIR = os.path.join(HOME, "device_configs")
LOG_DIR = os.path.join(HOME, "deploy_logs")
UTF16_FILE = os.path.join(CFG_DIR, "config_utf16.txt")
UTF8_FILE = os.path.join(CFG_DIR, "config_utf8.txt")
CHECKSUM_LOG = os.path.join(LOG_DIR, "config_checksums.log")

EXPECTED_TEXT = (
    "device_id=alpha123\n"
    "firmware=1.04\n"
    "mode=active\n"
    "# end of file\n"
)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _mode(path):
    "Return the permission bits (e.g. 0o700, 0o644) of a filesystem entry."
    return stat.S_IMODE(os.lstat(path).st_mode)

def _assert_perms(path, expected, note=""):
    perm = _mode(path)
    assert perm == expected, (
        f"{path} should have permissions {oct(expected)}, "
        f"but has {oct(perm)}. {note}"
    )

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directories_exist_and_permissions():
    # device_configs directory
    assert os.path.isdir(CFG_DIR), f"Required directory {CFG_DIR} is missing."
    _assert_perms(
        CFG_DIR,
        0o700,
        "Directory should be private (rwx------) as per specification.",
    )

    # deploy_logs directory
    assert os.path.isdir(LOG_DIR), f"Required directory {LOG_DIR} is missing."
    _assert_perms(
        LOG_DIR,
        0o700,
        "Directory should be private (rwx------) as per specification.",
    )


def test_utf16_seed_file_properties():
    # Presence
    assert os.path.isfile(
        UTF16_FILE
    ), f"Seed configuration file {UTF16_FILE} is missing."

    # Permissions: exactly 0644 (or more restrictive, i.e. <= 0644)
    actual_mode = _mode(UTF16_FILE)
    assert actual_mode & 0o777 <= 0o644, (
        f"{UTF16_FILE} permissions are {oct(actual_mode)}, "
        "but they must be 0644 or more restrictive."
    )

    # BOM & encoding check
    with open(UTF16_FILE, "rb") as fh:
        raw = fh.read()

    assert raw.startswith(
        b"\xff\xfe"
    ), f"{UTF16_FILE} must start with UTF-16LE BOM 0xFF 0xFE."

    # Decode using 'utf-16' (which honours BOM) to verify content.
    try:
        decoded = raw.decode("utf-16")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{UTF16_FILE} could not be decoded as UTF-16LE: {exc}")

    assert (
        decoded == EXPECTED_TEXT
    ), f"{UTF16_FILE} textual content does not match the required lines."

    # Ensure only LF (\\n) line terminators are present.
    assert "\r" not in decoded, (
        f"{UTF16_FILE} contains CR characters; only LF (\\n) is allowed."
    )

    # Sanity-check: four lines + trailing newline.
    lines = decoded.splitlines(keepends=False)
    assert len(lines) == 4, (
        f"{UTF16_FILE} should contain 4 logical lines, found {len(lines)}."
    )
    assert lines[-1].startswith("# end of file"), (
        f"The last line of {UTF16_FILE} should be '# end of file'."
    )


def test_output_files_absent_initially():
    # UTF-8 version should NOT exist yet
    assert not os.path.exists(
        UTF8_FILE
    ), f"{UTF8_FILE} should NOT exist before the student runs their solution."

    # Checksum log should NOT exist yet
    assert not os.path.exists(
        CHECKSUM_LOG
    ), f"{CHECKSUM_LOG} should NOT exist before the student runs their solution."