# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present **before** the student begins their work on the FinOps files.
#
# What we check:
#   • Presence of /home/user/finops directory.
#   • Presence, permissions and exact contents of the two config files:
#       - /home/user/finops/cost_policy.yaml
#       - /home/user/finops/subscription.toml
#   • Absence of the log file that will be created later:
#       - /home/user/finops/update_log.txt
#
# All failures raise clear, actionable messages.
#
# Only stdlib + pytest are used.

import os
import stat
from pathlib import Path
import hashlib
import pytest

FINOPS_DIR = Path("/home/user/finops")
YAML_FILE = FINOPS_DIR / "cost_policy.yaml"
TOML_FILE = FINOPS_DIR / "subscription.toml"
LOG_FILE = FINOPS_DIR / "update_log.txt"


# --------------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------------
def sha256_of(text: str) -> str:
    """Return the SHA-256 hex-digest of the given UTF-8 string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def assert_permissions(path: Path, expected_mode: int) -> None:
    """Assert that a file has exactly the expected octal permissions."""
    mode = path.stat().st_mode & 0o777
    assert mode == expected_mode, (
        f"{path} permissions are {oct(mode)}, expected {oct(expected_mode)}"
    )


# --------------------------------------------------------------------------
# Expected *initial* file contents
# --------------------------------------------------------------------------
EXPECTED_YAML_CONTENT = (
    "environments:\n"
    "  dev:\n"
    "    monthly_budget: 300\n"
    "  prod:\n"
    "    monthly_budget: 1200\n"
)

EXPECTED_TOML_CONTENT = (
    "[features]\n"
    "spot_instances = false\n"
    "commitment_discounts = false\n"
    "rightsizing = false\n"
    "\n"
    "[limits]\n"
    "max_instances = 50\n"
    "max_cores = 200\n"
)

EXPECTED_YAML_SHA256 = sha256_of(EXPECTED_YAML_CONTENT)
EXPECTED_TOML_SHA256 = sha256_of(EXPECTED_TOML_CONTENT)


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
def test_finops_directory_exists():
    assert FINOPS_DIR.is_dir(), f"Required directory {FINOPS_DIR} does not exist."


def test_cost_policy_yaml_initial_state():
    # File existence
    assert YAML_FILE.is_file(), f"Missing initial file: {YAML_FILE}"

    # Permissions (0644)
    assert_permissions(YAML_FILE, 0o644)

    # Content and checksum
    actual_text = YAML_FILE.read_text(encoding="utf-8")
    assert (
        actual_text == EXPECTED_YAML_CONTENT
    ), (
        f"{YAML_FILE} content mismatch:\n"
        f"--- expected SHA256: {EXPECTED_YAML_SHA256}\n"
        f"+++ actual   SHA256: {sha256_of(actual_text)}\n"
        "File must match the exact starter content provided in the task description."
    )


def test_subscription_toml_initial_state():
    # File existence
    assert TOML_FILE.is_file(), f"Missing initial file: {TOML_FILE}"

    # Permissions (0644)
    assert_permissions(TOML_FILE, 0o644)

    # Content and checksum
    actual_text = TOML_FILE.read_text(encoding="utf-8")
    assert (
        actual_text == EXPECTED_TOML_CONTENT
    ), (
        f"{TOML_FILE} content mismatch:\n"
        f"--- expected SHA256: {EXPECTED_TOML_SHA256}\n"
        f"+++ actual   SHA256: {sha256_of(actual_text)}\n"
        "File must match the exact starter content provided in the task description."
    )


def test_update_log_absent():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist before the student performs any actions."
    )