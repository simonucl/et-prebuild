# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem
# is in the correct *initial* state **before** the student performs
# any actions for the “dashboard tuning” exercise.
#
# It deliberately does NOT test for the presence (or absence) of any
# files or directories that the student is expected to create later
# (e.g. /home/user/observability/dashboard/… or tuning.log).
#
# Only the baseline template directory and file are inspected.

from pathlib import Path
import hashlib
import pytest

HOME = Path("/home/user")
TEMPLATES_DIR = HOME / "observability" / "templates"
TEMPLATE_FILE = TEMPLATES_DIR / "metrics_base.json"


# The exact contents that must be present in
# /home/user/observability/templates/metrics_base.json
EXPECTED_TEMPLATE_CONTENT = (
    '{\n'
    '  "id": null,\n'
    '  "title": "Base Metrics Dashboard",\n'
    '  "uid": "base-metrics",\n'
    '  "tags": [\n'
    '    "base"\n'
    '  ],\n'
    '  "refresh": "10s",\n'
    '  "panels": []\n'
    '}\n'
)

# Pre-computed SHA-256 hash of the expected content above.
EXPECTED_TEMPLATE_SHA256 = hashlib.sha256(
    EXPECTED_TEMPLATE_CONTENT.encode("utf-8")
).hexdigest()


def test_templates_directory_exists():
    """The templates directory must exist and be a directory."""
    assert TEMPLATES_DIR.exists(), (
        f"Required directory missing: {TEMPLATES_DIR}"
    )
    assert TEMPLATES_DIR.is_dir(), (
        f"Expected {TEMPLATES_DIR} to be a directory."
    )


def test_metrics_base_json_exists_and_content_is_exact():
    """
    The baseline dashboard template must exist and its contents must match
    the precise JSON (byte-for-byte, including whitespace and trailing newline).
    """
    assert TEMPLATE_FILE.exists(), (
        f"Required file missing: {TEMPLATE_FILE}"
    )
    assert TEMPLATE_FILE.is_file(), (
        f"Expected {TEMPLATE_FILE} to be a regular file."
    )

    actual_content = TEMPLATE_FILE.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_TEMPLATE_CONTENT, (
        "The contents of metrics_base.json do not match the expected template.\n"
        "If the file has been modified, replace it with the original content shown "
        "in the task description."
    )

    # Additional guard: compare SHA-256 to surface hidden whitespace changes.
    actual_sha256 = hashlib.sha256(actual_content.encode("utf-8")).hexdigest()
    assert actual_sha256 == EXPECTED_TEMPLATE_SHA256, (
        "SHA-256 hash mismatch for metrics_base.json ‑ possible hidden differences "
        "(whitespace, newlines, encoding)."
    )