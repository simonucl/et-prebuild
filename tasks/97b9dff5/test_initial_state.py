# test_initial_state.py
"""
Pytest suite to validate the initial operating-system / filesystem state
BEFORE the learner begins the “network-automation” exercise.

Only pre-existing artefacts are inspected.  Nothing related to the
EXPECTED output (e.g. /home/user/troubleshoot/ or any log files that
will be created later) is referenced in this test file.

All assertions include clear, actionable failure messages.
"""
from pathlib import Path
import re

import pytest

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
BASE_DIR = Path("/home/user/network_configs")
ROUTER_FILE = BASE_DIR / "router.yml"
FIREWALL_FILE = BASE_DIR / "firewall.toml"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    """Return file contents or raise a pytest failure with a helpful message."""
    if not path.exists():
        pytest.fail(f"Expected file to exist but it is missing: {path}")
    if not path.is_file():
        pytest.fail(f"Expected a regular file at {path}, but found something else.")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_network_configs_directory_exists():
    """The /home/user/network_configs directory must exist and be a directory."""
    assert BASE_DIR.exists(), f"Directory missing: {BASE_DIR}"
    assert BASE_DIR.is_dir(), f"Expected {BASE_DIR} to be a directory."


def test_router_yml_initial_contents():
    """
    router.yml must:
    * exist
    * contain the two original DNS servers
    * NOT contain 8.8.8.8
    * keep the indentation / formatting shown in the exercise description
    """
    content = read_text(ROUTER_FILE)

    # Basic sanity check: 'network:' top-level key present.
    assert re.search(r"^network:", content, re.MULTILINE), (
        "router.yml does not appear to contain the top-level 'network:' key."
    )

    # Verify both original DNS servers are present.
    for dns in ("1.1.1.1", "9.9.9.9"):
        assert f"- {dns}" in content, (
            f"router.yml is missing the DNS server {dns}. "
            "File should list both 1.1.1.1 and 9.9.9.9."
        )

    # Verify that 8.8.8.8 has NOT yet been added.
    assert "8.8.8.8" not in content, (
        "router.yml already contains 8.8.8.8, "
        "but this should only be added by the learner."
    )

    # Very rough indentation check (2-space indents for DNS list).
    dns_lines = [line for line in content.splitlines() if re.match(r"\s*-\s*\d+\.\d+\.\d+\.\d+/?\d*", line)]
    for line in dns_lines:
        assert line.startswith("    - ") or line.startswith("  - "), (
            "DNS list items should use 2-space indentation (e.g. '  - 1.1.1.1'). "
            f"Offending line: {line!r}"
        )


def test_firewall_toml_initial_contents():
    """
    firewall.toml must:
    * exist
    * allow ports 22 and 80 (tcp) only
    * NOT yet allow port 443
    """
    content = read_text(FIREWALL_FILE)

    # Make sure the default policy block exists.
    assert "[default]" in content, "firewall.toml missing the [default] policy block."

    # Verify port 22 and 80 rules exist.
    for port in (22, 80):
        regex = rf"port\s*=\s*{port}"
        assert re.search(regex, content), (
            f"firewall.toml missing rule that opens port {port}."
        )

    # Ensure port 443 has NOT been opened yet.
    assert "port = 443" not in content, (
        "firewall.toml already contains a rule for port 443, "
        "but this should only be added by the learner."
    )

    # Count the number of [[rule]] blocks (should be 2 at this point).
    rule_blocks = re.findall(r"^\[\[rule]]", content, flags=re.MULTILINE)
    assert len(rule_blocks) == 2, (
        "firewall.toml should contain exactly two [[rule]] blocks (for ports 22 and 80) "
        f"before the learner starts, but found {len(rule_blocks)}."
    )