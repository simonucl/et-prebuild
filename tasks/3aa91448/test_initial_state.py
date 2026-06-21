# test_initial_state.py
#
# This test-suite validates ONLY the **initial state** that must be
# present *before* the student starts working.  It deliberately avoids
# checking for any of the artefacts that the student is expected to
# create later (e.g. firewall_logs/, active_rules.v4, the CSV file, …).

import ipaddress
from pathlib import Path
import pytest

HOME = Path("/home/user")

# ---------- Paths that must already exist ----------
INITIAL_RULES = HOME / "firewall_rules" / "initial_rules.v4"
RAW_PCAP      = HOME / "logs" / "packet.log"


def test_required_paths_exist_and_are_readable():
    """
    Ensure the two mandatory pre-existing files are present and readable.
    """
    for path in (INITIAL_RULES, RAW_PCAP):
        assert path.exists(), f"Expected file {path} does not exist."
        assert path.is_file(), f"{path} exists but is not a regular file."
        # try opening for read to guarantee permissions
        with path.open("r", encoding="utf-8") as fh:
            fh.read(0)


# ---------------------------------------------------------------------
# Firewall rules sanity checks
# ---------------------------------------------------------------------
def _read_nonempty_lines(path: Path):
    """Return a list of non-blank, stripped lines from *path*."""
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()
            if ln.strip()]


def test_initial_ruleset_has_expected_tail():
    """
    The initial IPv4 ruleset must end with the wide-open ACCEPT rule that the
    student will later precede with DROP rules; final non-comment line should
    be '-A INPUT -p tcp -j ACCEPT' followed by 'COMMIT'.
    """
    lines = _read_nonempty_lines(INITIAL_RULES)

    # A valid iptables-save file starts with '*filter' and ends with 'COMMIT'
    assert lines[0] == "*filter", (
        f"{INITIAL_RULES} should start with '*filter'; found {lines[0]!r}"
    )
    assert lines[-1] == "COMMIT", (
        f"{INITIAL_RULES} must end with 'COMMIT'; found {lines[-1]!r}"
    )

    # The line just before COMMIT must be the wide-open rule
    wide_open = "-A INPUT -p tcp -j ACCEPT"
    assert lines[-2] == wide_open, (
        "Expected the wide-open rule to be the last rule before COMMIT "
        f"but found {lines[-2]!r}."
    )

    # It should appear exactly once
    occurrences = [i for i, ln in enumerate(lines) if ln == wide_open]
    assert len(occurrences) == 1, (
        f"Wide-open rule {wide_open!r} appears {len(occurrences)} times, "
        "but should appear exactly once."
    )

    # There must be *no* DROP rules yet
    drops = [ln for ln in lines if " -j DROP" in ln]
    assert not drops, (
        f"Initial ruleset already contains DROP rules, which is unexpected: {drops}"
    )


# ---------------------------------------------------------------------
# Packet log sanity checks
# ---------------------------------------------------------------------
TARGET_HOST = ipaddress.ip_address("203.0.113.45")
TARGET_NET  = ipaddress.ip_network("198.51.100.0/24")


def _extract_src_ip(line: str):
    """
    Very lightweight parser: look for the substring 'SRC=' and return the
    immediately following token.
    """
    marker = "SRC="
    try:
        start = line.index(marker) + len(marker)
    except ValueError:
        return None
    # an IP ends at first space or end-of-line
    end = line.find(" ", start)
    if end == -1:
        end = len(line)
    return line[start:end]


def test_packet_log_contains_expected_counts():
    """
    Verify that the sample packet capture has the six lines and distribution
    documented in the task description.  This ensures the student’s later
    counting logic will run against known input.
    """
    lines = [ln.strip() for ln in RAW_PCAP.read_text(encoding="utf-8").splitlines()
             if ln.strip()]

    assert len(lines) == 6, (
        f"Expected exactly 6 non-blank lines in {RAW_PCAP}, found {len(lines)}."
    )

    counts = {}
    for ln in lines:
        src = _extract_src_ip(ln)
        assert src, f"Line missing 'SRC=' field: {ln!r}"
        counts[src] = counts.get(src, 0) + 1

    # Expected distribution
    expected = {
        "203.0.113.45": 3,
        "198.51.100.23": 2,
        "198.51.100.47": 1,
    }

    assert counts == expected, (
        "Packet log source counts do not match the expected initial state.\n"
        f"Expected: {expected}\n"
        f"Found   : {counts}"
    )

    # Sanity: ensure all logged IPs fall into the host or subnet of interest
    for ip_str in counts:
        ip_obj = ipaddress.ip_address(ip_str)
        assert ip_obj == TARGET_HOST or ip_obj in TARGET_NET, (
            f"Found unexpected source IP in log: {ip_str}"
        )