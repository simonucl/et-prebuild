# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem state that must exist
# BEFORE the student modifies anything.  It checks that the original
# firewall files are present and strictly correct, and also that the
# yet-to-be-created artefacts do **not** exist.

import os
import stat
from pathlib import Path
import textwrap
import pytest

HOME = Path("/home/user")
FW_DIR = HOME / "firewall"

CURRENT_RULES = FW_DIR / "current_rules.v4"
PROPOSED_RULES = FW_DIR / "proposed_rules.v4"
CHANGE_LOG = FW_DIR / "config_changes.log"


@pytest.fixture(scope="module")
def expected_current_rules_text() -> str:
    """
    The exact, byte-for-byte contents required for the original
    `/home/user/firewall/current_rules.v4` file.
    A trailing newline **is** expected.
    """
    return textwrap.dedent(
        """\
        *filter
        :INPUT DROP [0:0]
        :FORWARD DROP [0:0]
        :OUTPUT ACCEPT [0:0]
        -A INPUT  -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
        -A INPUT  -p icmp -j ACCEPT
        -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
        -A FORWARD -s 10.10.10.0/24   -p tcp -m tcp --dport 22  -j ACCEPT
        -A FORWARD -j DROP
        COMMIT
        """
    )


# --------------------------------------------------------------------------- #
# Directory checks
# --------------------------------------------------------------------------- #
def test_firewall_directory_exists_and_mode():
    assert FW_DIR.exists(), (
        f"Expected directory {FW_DIR} to exist, "
        "but it is missing."
    )
    assert FW_DIR.is_dir(), f"{FW_DIR} exists but is not a directory."

    mode = stat.S_IMODE(FW_DIR.stat().st_mode)
    assert mode == 0o700, (
        f"{FW_DIR} permissions are {oct(mode)}, expected 0o700."
    )


# --------------------------------------------------------------------------- #
# File: current_rules.v4
# --------------------------------------------------------------------------- #
def test_current_rules_file_exists_and_mode():
    assert CURRENT_RULES.exists(), (
        f"Expected file {CURRENT_RULES} to exist, "
        "but it is missing."
    )
    assert CURRENT_RULES.is_file(), f"{CURRENT_RULES} exists but is not a regular file."

    mode = stat.S_IMODE(CURRENT_RULES.stat().st_mode)
    assert mode == 0o600, (
        f"{CURRENT_RULES} permissions are {oct(mode)}, expected 0o600."
    )


def test_current_rules_file_contents(expected_current_rules_text):
    file_text = CURRENT_RULES.read_text(encoding="utf-8")

    # We require an exact match including whitespace except for
    # a single trailing newline at EOF, which is normalised here.
    assert (
        file_text.rstrip("\n") == expected_current_rules_text.rstrip("\n")
    ), (
        f"Contents of {CURRENT_RULES} do not match the expected "
        "initial iptables-save rules."
    )


# --------------------------------------------------------------------------- #
# Files that must *NOT* exist yet
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path,description",
    [
        (PROPOSED_RULES, "proposed_rules.v4"),
        (CHANGE_LOG, "config_changes.log"),
    ],
)
def test_future_files_do_not_exist(path: Path, description: str):
    assert not path.exists(), (
        f"The file {path} ({description}) should NOT exist before the student "
        "performs any actions, but it is already present."
    )