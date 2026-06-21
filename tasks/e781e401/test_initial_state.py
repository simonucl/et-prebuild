# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the operating system / file
# system *before* the student starts working on the task “Profile and document
# local hostname resolution”.
#
# What we check:
#   1. The project directory /home/user/dns_profile exists.
#   2. The file /home/user/dns_profile/custom_hosts exists.
#   3. custom_hosts has the correct permissions (0644).
#   4. custom_hosts contains exactly the three expected IPv4-to-hostname
#      mappings and nothing else.
#
# We deliberately do **not** check for any artefacts that should be created by
# the student later (e.g. the additional mapping or the
# hostname_resolution.log file).

import os
import stat
import pytest

DIR_PATH = "/home/user/dns_profile"
HOSTS_FILE = os.path.join(DIR_PATH, "custom_hosts")

EXPECTED_LINES = [
    "192.168.50.10 app.internal.local app",
    "192.168.50.11 db.internal.local db",
    "192.168.50.12 cache.internal.local cache",
]

@pytest.mark.order(1)
def test_dns_profile_directory_exists():
    assert os.path.isdir(DIR_PATH), (
        f"Required directory {DIR_PATH!r} is missing. "
        "The starter project should provide it."
    )

@pytest.mark.order(2)
def test_custom_hosts_file_exists():
    assert os.path.isfile(HOSTS_FILE), (
        f"Required file {HOSTS_FILE!r} is missing. "
        "The starter project should include it."
    )

@pytest.mark.order(3)
def test_custom_hosts_file_permissions():
    mode = stat.S_IMODE(os.stat(HOSTS_FILE).st_mode)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"{HOSTS_FILE!r} should have permissions {oct(expected_mode)}, "
        f"but has {oct(mode)}."
    )

@pytest.mark.order(4)
def test_custom_hosts_file_content():
    with open(HOSTS_FILE, "r", encoding="utf-8") as f:
        # Strip trailing newlines; ignore any completely blank lines.
        lines = [ln.rstrip("\n") for ln in f.readlines() if ln.strip()]

    assert lines == EXPECTED_LINES, (
        f"{HOSTS_FILE!r} content is not as expected.\n"
        f"Expected exactly:\n{EXPECTED_LINES}\n"
        f"Found:\n{lines}"
    )