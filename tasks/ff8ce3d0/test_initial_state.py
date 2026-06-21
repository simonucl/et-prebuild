# test_initial_state.py
#
# This test-suite asserts the expected *initial* filesystem state
# before the engineer makes any modifications.  If any of these tests
# fail it means the starting snapshot is not what the assignment
# describes, so the follow-up verification will be unreliable.
#
# Only the Python stdlib and pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Paths used throughout the checks
# ---------------------------------------------------------------------------
FIREWALL_DIR = HOME / "firewall"
ACTIVE_RULES = FIREWALL_DIR / "active_rules.conf"
LOGS_DIR = FIREWALL_DIR / "logs"          # must NOT exist yet
STATUS_LOG = LOGS_DIR / "firewall_status.log"

LOCALISE_DIR = HOME / "localise-site"
TEMPLATE_FILE = LOCALISE_DIR / "templates" / "messages.pot"
FRENCH_PO = LOCALISE_DIR / "fr.po"


# ---------------------------------------------------------------------------
# Expected baseline contents
# ---------------------------------------------------------------------------
EXPECTED_ACTIVE_RULES = (
    "# Firewall Rules\n"
    "# -----------------------------------------------------------------------------\n"
    "# default policy : deny incoming, allow outgoing\n"
    "# -----------------------------------------------------------------------------\n"
    "# BEGIN RULES\n"
    "# END RULES\n"
)

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_firewall_directory_exists():
    assert FIREWALL_DIR.is_dir(), f"Missing directory: {FIREWALL_DIR}"


def test_active_rules_file_has_expected_content():
    assert ACTIVE_RULES.is_file(), f"Missing file: {ACTIVE_RULES}"
    content = ACTIVE_RULES.read_text(encoding="utf-8")
    assert content == EXPECTED_ACTIVE_RULES, (
        f"{ACTIVE_RULES} contents differ from the expected baseline.\n"
        "If the file already contains the new rule or any other change, "
        "reset it to the six-line template provided in the specification."
    )


def test_no_logs_directory_yet():
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} should not exist before any firewall changes are logged."
    )


def test_localise_project_structure():
    # Project root must exist
    assert LOCALISE_DIR.is_dir(), f"Missing localisation directory: {LOCALISE_DIR}"

    # Template directory and file must exist
    template_dir = TEMPLATE_FILE.parent
    assert template_dir.is_dir(), f"Missing template directory: {template_dir}"
    assert TEMPLATE_FILE.is_file(), f"Missing template file: {TEMPLATE_FILE}"

    # Template file must have at least 17 lines (header section)
    with TEMPLATE_FILE.open(encoding="utf-8") as fh:
        lines = fh.readlines()
    assert len(lines) >= 17, (
        f"{TEMPLATE_FILE} is expected to have at least 17 lines for the header; "
        f"found only {len(lines)}."
    )


def test_no_french_translation_exists_yet():
    assert not FRENCH_PO.exists(), (
        f"{FRENCH_PO} should NOT exist before the engineer creates the French translation."
    )


def test_no_status_log_file_yet():
    assert not STATUS_LOG.exists(), (
        f"{STATUS_LOG} should not exist prior to any firewall modification."
    )