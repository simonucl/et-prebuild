# test_initial_state.py
#
# This pytest suite validates the **pre-existing** operating-system / filesystem
# state before the student performs any action.  It checks only what must
# already be in place: the /home/user/cloud directory and the exact content of
# /home/user/cloud/services.ini.  It deliberately does **not** look for any of
# the files the student is expected to create (production_services.txt,
# extract.log, etc.).

import os
import stat
import pytest

CLOUD_DIR = "/home/user/cloud"
SERVICES_INI = os.path.join(CLOUD_DIR, "services.ini")

# The exact, byte-for-byte content that must already be present in services.ini
EXPECTED_INI_CONTENT = (
    "[development]\n"
    "db=dev-db.internal\n"
    "cache=dev-cache.internal\n"
    "api=dev-api.internal\n"
    "\n"
    "[staging]\n"
    "db=stage-db.internal\n"
    "cache=stage-cache.internal\n"
    "api=stage-api.internal\n"
    "\n"
    "[production]\n"
    "db=prod-db.internal\n"
    "cache=prod-cache.internal\n"
    "api=prod-api.internal\n"
    "search=prod-search.internal\n"
    "worker=prod-worker.internal\n"
)

def test_cloud_directory_exists_and_is_accessible():
    """The /home/user/cloud directory must exist and be user-accessible."""
    assert os.path.isdir(CLOUD_DIR), (
        f"Required directory missing: {CLOUD_DIR!r}.\n"
        "Create it (with user read/write/execute permissions) before continuing."
    )

    # Basic permission check: user should have rwx (at least r-x for existence).
    mode = os.stat(CLOUD_DIR).st_mode
    user_perms = stat.S_IMODE(mode) & stat.S_IRWXU
    expected = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
    assert user_perms & expected == expected, (
        f"The directory {CLOUD_DIR!r} does not grant the user rwx permissions."
    )

def test_services_ini_exists():
    """services.ini must exist inside /home/user/cloud."""
    assert os.path.isfile(SERVICES_INI), (
        f"Required file missing: {SERVICES_INI!r}.\n"
        "Ensure the legacy configuration file is in place before proceeding."
    )

def test_services_ini_exact_content():
    """
    services.ini must contain the exact expected byte sequence:
    • UNIX newlines only (\\n)
    • No carriage returns (\\r)
    • No trailing spaces on any line
    • File must end with a single newline
    """
    with open(SERVICES_INI, "rb") as fp:
        content_bytes = fp.read()

    # 1. No CR characters
    assert b"\r" not in content_bytes, (
        f"{SERVICES_INI!r} contains Windows-style CR characters (\\r); "
        "it should use UNIX newlines only."
    )

    content = content_bytes.decode("utf-8")

    # 2. Exact content match
    assert content == EXPECTED_INI_CONTENT, (
        f"The contents of {SERVICES_INI!r} do not match the expected legacy "
        "configuration.\n"
        "Differences may include extra/missing lines, incorrect hostnames, "
        "or unexpected whitespace."
    )

    # 3. Verify no trailing spaces at line ends
    for i, line in enumerate(content.split("\n")[:-1], start=1):  # ignore final empty string from split
        assert line == line.rstrip(" "), (
            f"Line {i} in {SERVICES_INI!r} has trailing spaces: {line!r}"
        )

    # 4. Ensure file ends with exactly one newline
    assert content.endswith("\n") and not content.endswith("\n\n"), (
        f"{SERVICES_INI!r} must end with exactly one newline (\\n)."
    )