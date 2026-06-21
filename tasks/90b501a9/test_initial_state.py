# test_initial_state.py
#
# Pytest suite to validate the starting state of the filesystem *before*
# the student makes any changes.  These tests assert that:
#
# 1. /home/user/monitoring/conf/alerts.yaml exists, contains the expected
#    stock content (header, disk_space_low alert, marker) and does *not*
#    yet contain the new high_cpu alert block.
#
# 2. /home/user/monitoring/conf/thresholds.toml exists, contains the
#    [global] table and marker, and does *not* yet contain the new
#    [alert.high_cpu] table.
#
# 3. /home/user/monitoring/logs/ exists as a directory and is empty
#    (config_update.log must not be present).
#
# These assertions guarantee that the learner starts from a clean, known
# baseline.  Any failure message should immediately pinpoint what piece
# of required initial state is missing or has been pre-modified.


import io
from pathlib import Path

import pytest


HOME = Path("/home/user")
CONF_DIR = HOME / "monitoring" / "conf"
LOG_DIR = HOME / "monitoring" / "logs"

ALERTS_YAML = CONF_DIR / "alerts.yaml"
THRESHOLDS_TOML = CONF_DIR / "thresholds.toml"
LOG_FILE = LOG_DIR / "config_update.log"


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def read_text(path: Path) -> str:
    """Read a file as UTF-8 text.

    A nicer helper solely to centralise the encoding and error handling.
    """
    try:
        with io.open(path, "r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError as exc:
        pytest.fail(f"Expected file {path} is missing.")  # pragma: no cover


# ----------------------------------------------------------------------
# Tests for alerts.yaml
# ----------------------------------------------------------------------
def test_alerts_yaml_exists():
    """alerts.yaml must exist at the exact absolute path."""
    assert ALERTS_YAML.is_file(), (
        f"{ALERTS_YAML} is expected to exist but was not found."
    )


def test_alerts_yaml_has_expected_baseline():
    """Validate header, disk_space_low alert, marker, and absence of high_cpu."""
    content = read_text(ALERTS_YAML)
    lines = content.splitlines()

    # 1) File must start with the header comment.
    assert lines and lines[0].strip() == "# Managed by monitoring team", (
        f"{ALERTS_YAML} should start with '# Managed by monitoring team' "
        f"but first line was: {lines[0] if lines else '<empty file>'}"
    )

    # 2) The predefined disk_space_low alert must be present.
    assert "- name: disk_space_low" in content, (
        "'disk_space_low' alert block not found in alerts.yaml; "
        "baseline content appears to be incorrect."
    )

    # 3) The marker for new alerts must exist.
    marker = "# --- ADD NEW ALERTS BELOW THIS LINE ---"
    assert marker in content, (
        f"Marker line '{marker}' is missing from alerts.yaml."
    )

    # 4) The new high_cpu alert must NOT yet exist.
    assert "- name: high_cpu" not in content, (
        "alerts.yaml already contains '- name: high_cpu' but it should not be "
        "present before the student performs any action."
    )


# ----------------------------------------------------------------------
# Tests for thresholds.toml
# ----------------------------------------------------------------------
def test_thresholds_toml_exists():
    """thresholds.toml must exist at the exact absolute path."""
    assert THRESHOLDS_TOML.is_file(), (
        f"{THRESHOLDS_TOML} is expected to exist but was not found."
    )


def test_thresholds_toml_has_expected_baseline():
    """Validate [global] table, marker, and absence of [alert.high_cpu] block."""
    content = read_text(THRESHOLDS_TOML)

    # 1) The [global] table must be present.
    assert "[global]" in content, (
        "The '[global]' table is missing from thresholds.toml."
    )

    # 2) The marker for new alert thresholds must be present.
    marker = "# --- ADD ALERT THRESHOLDS BELOW THIS LINE ---"
    assert marker in content, (
        f"Marker line '{marker}' is missing from thresholds.toml."
    )

    # 3) The new [alert.high_cpu] block must NOT yet be present.
    assert "[alert.high_cpu]" not in content, (
        "thresholds.toml already contains '[alert.high_cpu]' but it should not "
        "be present before the student performs any action."
    )


# ----------------------------------------------------------------------
# Tests for logs directory
# ----------------------------------------------------------------------
def test_logs_directory_exists_and_empty():
    """Log directory must exist and be empty."""
    assert LOG_DIR.is_dir(), (
        f"Expected log directory {LOG_DIR} to exist but it was not found."
    )

    files = list(LOG_DIR.iterdir())
    assert not files, (
        f"Log directory {LOG_DIR} should be empty initially, "
        f"but found: {[p.name for p in files]}"
    )

    # Specifically ensure config_update.log does not pre-exist.
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should not exist before the student's changes."
    )