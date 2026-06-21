# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state for the
“Disable inbound Telnet” exercise **before** the student runs a single
command.

If any of these tests fail, the grading container itself is mis-provisioned
and the student should not be penalised.

Only the Python stdlib and pytest are used.
"""

from pathlib import Path
import pytest
import hashlib
import textwrap

HOME = Path("/home/user")
NET_DIR = HOME / "network"
RULES_FILE = NET_DIR / "firewall_rules.conf"
BACKUP_FILE = NET_DIR / "firewall_rules.conf.bak"
LOG_FILE = NET_DIR / "remediation.log"
NMAP_FILE = NET_DIR / "nmap_scan.txt"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def sha256(path: Path) -> str:
    """Return the hex‐encoded SHA-256 of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Expected baseline artefacts
# ---------------------------------------------------------------------------

EXPECTED_RULES_CONTENT = textwrap.dedent(
    """\
    # Simulated iptables-save output generated on 2024-01-01
    *filter
    :INPUT DROP [0:0]
    :FORWARD DROP [0:0]
    :OUTPUT ACCEPT [0:0]
    -A INPUT -p tcp --dport 22 -j ACCEPT
    -A INPUT -p tcp --dport 23 -j ACCEPT
    -A INPUT -p tcp --dport 80 -j ACCEPT
    -A INPUT -j DROP
    COMMIT
    """
).encode()  # .encode() so we can check exact byte content including trailing \n

# SHA-256 of the expected file; keeps tests compact when we need an exact match
EXPECTED_RULES_SHA256 = hashlib.sha256(EXPECTED_RULES_CONTENT).hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directory_structure_exists():
    """/home/user/network must exist and be a directory."""
    assert NET_DIR.exists(), f"Required directory {NET_DIR} is missing."
    assert NET_DIR.is_dir(), f"{NET_DIR} exists but is not a directory."


def test_firewall_rules_file_exact_match():
    """firewall_rules.conf must exist and match the expected baseline *exactly*."""
    assert RULES_FILE.exists(), f"Cannot find required file {RULES_FILE}."
    assert RULES_FILE.is_file(), f"{RULES_FILE} exists but is not a regular file."

    data = RULES_FILE.read_bytes()
    sha = hashlib.sha256(data).hexdigest()

    # Helpful diff for minor problems
    if sha != EXPECTED_RULES_SHA256:
        # Provide a small hint of where it differs without dumping entire file
        expected_preview = EXPECTED_RULES_CONTENT.decode().splitlines(keepends=True)[:10]
        actual_preview = data.decode(errors="replace").splitlines(keepends=True)[:10]
        diff_hint = ["First 10 lines of expected vs. actual (for debugging):", "-" * 40,
                     "EXPECTED:", *expected_preview,
                     "-" * 40,
                     "ACTUAL:", *actual_preview]
        pytest.fail(
            f"{RULES_FILE} content does not match the expected baseline.\n"
            f"SHA-256 expected: {EXPECTED_RULES_SHA256}\n"
            f"SHA-256 actual:   {sha}\n"
            + "\n".join(diff_hint)
        )


def test_firewall_rules_semantics():
    """Baseline semantic checks: port-23 ACCEPT rule present and un-commented."""
    lines = RULES_FILE.read_text().splitlines()

    # Ensure exactly one ACCEPT rule for port 23 and that it is not commented.
    accept_23 = [ln for ln in lines if ln.strip() == "-A INPUT -p tcp --dport 23 -j ACCEPT"]
    assert len(accept_23) == 1, (
        "Initial ruleset must contain *exactly one* line "
        "'-A INPUT -p tcp --dport 23 -j ACCEPT' (uncommented)."
    )

    # Count all ACCEPT rules (used later by the remediation script)
    accept_rules = [ln for ln in lines if ln.startswith("-A INPUT") and ln.strip().endswith("ACCEPT")]
    assert len(accept_rules) == 3, (
        "Initial ruleset should contain exactly 3 '-A INPUT … ACCEPT' lines "
        f"(found {len(accept_rules)})."
    )

    # Ensure there is *no* DROP rule for port 23 yet
    drop_23 = [ln for ln in lines if ln.strip() == "-A INPUT -p tcp --dport 23 -j DROP"]
    assert not drop_23, (
        "Initial ruleset unexpectedly already contains a DROP rule for port 23; "
        "the student is supposed to add this."
    )


def test_backup_and_log_do_not_exist_yet():
    """Backup and remediation log must not pre-exist; student will create them."""
    assert not BACKUP_FILE.exists(), (
        f"Backup file {BACKUP_FILE} already exists. Initial state must *not* "
        "contain the .bak file."
    )
    assert not LOG_FILE.exists(), (
        f"Remediation log {LOG_FILE} already exists. It should be created by the student."
    )


def test_nmap_scan_file_present():
    """nmap_scan.txt should be present but is not otherwise validated here."""
    assert NMAP_FILE.exists(), f"Expected auxiliary file {NMAP_FILE} is missing."
    assert NMAP_FILE.is_file(), f"{NMAP_FILE} exists but is not a regular file."

    # Quick sanity check that the scan indeed lists port 23 as open
    content = NMAP_FILE.read_text()
    assert "23/tcp open  telnet" in content, (
        f"{NMAP_FILE} should show port 23 open so the remediation makes sense."
    )


# ---------------------------------------------------------------------------
# End of test_initial_state.py
# ---------------------------------------------------------------------------