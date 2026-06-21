# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system /
# filesystem ­— i.e. **before** the student has performed any work.  The checks
# focus on the monitoring configuration described in the assignment.
#
# We rely only on the Python standard-library and pytest.

import pathlib
import re

import pytest


MONITORING_DIR = pathlib.Path("/home/user/monitoring")
ALERTS_FILE = MONITORING_DIR / "alerts.yaml"
NOTIF_FILE = MONITORING_DIR / "notifications.toml"
CHANGELOG_FILE = MONITORING_DIR / "change_log.txt"

# --------------------------------------------------------------------------- #
# Expected file contents (as specified by the exercise).
# --------------------------------------------------------------------------- #

EXPECTED_ALERTS_CONTENT = [
    "alerts:",
    "  - name: cpu_high",
    "    threshold: 85",
    "    enabled: false",
    "  - name: memory_high",
    "    threshold: 90",
    "    enabled: false",
]

EXPECTED_NOTIF_CONTENT = [
    "[smtp]",
    "enabled = false",
    'server  = "smtp.example.com"',
    "port    = 587",
    'sender  = "monitor@example.com"',
    'recipients = ["admin@example.com"]',
]


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_file_lines(path: pathlib.Path):
    """
    Read a text file and return a list of lines with trailing newlines stripped.

    The helper guarantees that file is opened using UTF-8 and unix newlines only.
    """
    text = path.read_text(encoding="utf-8")
    # Reject CRLF endings early; this must be a pure LF file.
    assert "\r" not in text, f"{path} must use LF (\\n) line endings only."
    return text.splitlines()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_monitoring_directory_exists():
    assert MONITORING_DIR.is_dir(), (
        f"Directory {MONITORING_DIR} is missing. "
        "The initial environment should already contain this directory."
    )


def test_no_unexpected_files_present():
    """
    Only alerts.yaml and notifications.toml should be present at the outset.
    """
    expected_files = {"alerts.yaml", "notifications.toml"}
    actual_files = {p.name for p in MONITORING_DIR.iterdir() if p.is_file()}
    unexpected = actual_files - expected_files
    missing = expected_files - actual_files
    assert not missing, (
        f"Expected file(s) {', '.join(sorted(missing))} not found in "
        f"{MONITORING_DIR}."
    )
    assert not unexpected, (
        f"Unexpected file(s) present in {MONITORING_DIR}: "
        f"{', '.join(sorted(unexpected))}. "
        "The starting state must contain only the two specified files."
    )


def test_alerts_yaml_initial_state_exact_contents():
    assert ALERTS_FILE.is_file(), f"Missing file: {ALERTS_FILE}"
    lines = read_file_lines(ALERTS_FILE)

    # Verify no tab characters are used for indentation.
    assert not any("\t" in line for line in lines), (
        f"{ALERTS_FILE} must not contain tab characters; use two-space indents."
    )

    assert lines == EXPECTED_ALERTS_CONTENT, (
        f"{ALERTS_FILE} does not match the expected initial contents.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_ALERTS_CONTENT)
        + "\n\nActual:\n"
        + "\n".join(lines)
    )

    # Additional semantic checks — exactly two alert entries.
    bullet_lines = [ln for ln in lines if ln.strip().startswith("- name:")]
    assert len(bullet_lines) == 2, (
        f"{ALERTS_FILE} should start with exactly two alert entries "
        "(cpu_high & memory_high)."
    )


def test_notifications_toml_initial_state_exact_contents():
    assert NOTIF_FILE.is_file(), f"Missing file: {NOTIF_FILE}"
    lines = read_file_lines(NOTIF_FILE)

    # No tab validation again.
    assert not any("\t" in line for line in lines), (
        f"{NOTIF_FILE} must not contain tab characters; keep spaces as provided."
    )

    assert lines == EXPECTED_NOTIF_CONTENT, (
        f"{NOTIF_FILE} does not match the expected initial contents.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_NOTIF_CONTENT)
        + "\n\nActual:\n"
        + "\n".join(lines)
    )

    # Semantic check — enabled must be 'false'.
    enabled_line = next((ln for ln in lines if ln.startswith("enabled")), None)
    assert enabled_line and enabled_line.strip().endswith("false"), (
        f"'enabled' flag should be false in the initial {NOTIF_FILE}."
    )

    # Only one recipient initially.
    recipients_line = next(
        (ln for ln in lines if ln.startswith("recipients")), None
    )
    assert recipients_line is not None, "Missing 'recipients' line."
    recipients_match = re.search(r"\[(.*)\]", recipients_line)
    assert recipients_match, "Cannot parse the recipients list."
    recipients = [r.strip().strip('"') for r in recipients_match.group(1).split(",") if r.strip()]
    assert recipients == ["admin@example.com"], (
        f"Initial recipient list should contain exactly one address "
        f"('admin@example.com'), got {recipients!r}"
    )


def test_changelog_does_not_exist_yet():
    assert not CHANGELOG_FILE.exists(), (
        f"{CHANGELOG_FILE} should NOT exist in the initial state; "
        "it will be created by the student once configuration changes are made."
    )