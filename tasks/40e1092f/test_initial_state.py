# test_initial_state.py
#
# This pytest suite verifies that the starting environment for the
# “connectivity-report” exercise is correct *before* the student begins
# working.  It checks:
#
# 1. The raw ping-capture file exists at the required absolute path and is
#    non-empty.
# 2. The raw capture contains a clearly delimited statistics section for each
#    of the three targets that the student must summarise.
# 3. No pre-made solution file is already present (the student must create it).
#
# Only the Python standard library and pytest are used.

import pathlib
import re

import pytest

HOME = pathlib.Path("/home/user")
RAW_LOG = HOME / "network_raw.log"
SUMMARY_DIR = HOME / "network_diagnostics"
SUMMARY_FILE = SUMMARY_DIR / "connection_summary.log"


@pytest.fixture(scope="session")
def raw_text():
    """Return the full text of the raw ping log, if it exists."""
    if not RAW_LOG.exists():
        pytest.skip(f"Prerequisite file {RAW_LOG} is missing on this system.")
    return RAW_LOG.read_text(encoding="utf-8", errors="replace")


def test_raw_log_exists_and_not_empty():
    """The seed file must be present and contain data."""
    assert RAW_LOG.is_file(), (
        f"Expected raw capture file at {RAW_LOG!s}, but it is missing "
        "or is not a regular file."
    )
    size = RAW_LOG.stat().st_size
    assert size > 0, f"The raw capture file {RAW_LOG!s} is empty."


@pytest.mark.parametrize(
    "needle",
    [
        "--- 8.8.8.8 ping statistics ---",
        "--- 1.1.1.1 ping statistics ---",
        "example.com",
    ],
)
def test_raw_log_contains_required_hosts(raw_text, needle):
    """Each host’s statistics header must appear in the raw capture."""
    assert needle in raw_text, (
        f"Could not find the statistics header for '{needle}' in "
        f"{RAW_LOG!s}.  Verify that the raw log contains data for all "
        "three targets: 8.8.8.8, 1.1.1.1 and example.com."
    )


@pytest.mark.parametrize(
    "host, expect_rtt",
    [
        ("8.8.8.8", True),
        ("1.1.1.1", True),
        ("example.com", False),  # 100 % loss, no RTT block expected
    ],
)
def test_raw_log_has_correct_rtt_presence(raw_text, host, expect_rtt):
    """
    For the first two hosts an RTT line must be present, while for example.com
    (100 % packet loss) *no* RTT line should be present.
    """
    # Build a minimal, host-specific regex that includes up to two lines after
    # the header, so we stay local to each block.
    header_pattern = re.escape(f"--- {host}") + r".*?^"  # up to EOL
    block_regex = re.compile(header_pattern + r"(.+\n){0,5}", re.MULTILINE | re.DOTALL)
    match = block_regex.search(raw_text)
    assert (
        match
    ), f"Could not locate the statistics block for host '{host}' in {RAW_LOG!s}."

    block = match.group(0)
    has_rtt = "rtt min/avg/max" in block
    assert has_rtt is expect_rtt, (
        f"RTT line presence for host '{host}' is incorrect.\n"
        f"Expected RTT line present: {expect_rtt}; found: {has_rtt}.\n"
        "Check that the raw log is unaltered and complete."
    )


def test_summary_file_is_absent_initially():
    """
    The deliverable summary must *not* exist yet; the student will create it.
    """
    assert not SUMMARY_FILE.exists(), (
        f"Found {SUMMARY_FILE!s} already present.  The starting environment "
        "should not contain a pre-created connectivity summary."
    )