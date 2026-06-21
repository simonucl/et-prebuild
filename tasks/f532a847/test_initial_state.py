# test_initial_state.py
#
# This pytest suite validates the initial operating-system / filesystem
# state **before** the student performs any actions.
#
# It checks that:
#   1. /home/user/configs/app.ini exists and is readable.
#   2. The INI file contains a [Compliance] section with the keys
#      “gdpr” and “hipaa”, whose values are “true” and “false”
#      respectively (case-sensitive comparison to the truth file).
#   3. The audit log that the student is supposed to create
#      (/home/user/audit/compliance_audit.log) does **not** yet exist.
#
# Only Python stdlib + pytest are used.

import configparser
from pathlib import Path

CONFIG_PATH = Path("/home/user/configs/app.ini")
AUDIT_LOG_PATH = Path("/home/user/audit/compliance_audit.log")


def test_config_file_exists():
    """
    The configuration file must exist at the exact absolute path so that the
    student script can read it.
    """
    assert CONFIG_PATH.is_file(), (
        f"Expected config file at {CONFIG_PATH} to exist, "
        f"but it was not found."
    )


def _load_config():
    """Helper that parses the INI file and returns a ConfigParser instance."""
    parser = configparser.ConfigParser()
    # Preserve case of keys for stricter comparison.
    parser.optionxform = str  # type: ignore[attr-defined]
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        parser.read_file(fh)
    return parser


def test_compliance_section_present():
    """
    The [Compliance] section must be present; otherwise the student would not
    have anything to parse.
    """
    parser = _load_config()
    assert parser.has_section(
        "Compliance"
    ), "[Compliance] section missing from /home/user/configs/app.ini"


def test_compliance_keys_and_values():
    """
    Ensure the gdpr and hipaa keys exist in the [Compliance] section and have
    the expected truth-file values.
    """
    parser = _load_config()
    compliance = parser["Compliance"]

    missing_keys = [k for k in ("gdpr", "hipaa") if k not in compliance]
    assert not missing_keys, (
        "The following key(s) are missing from the [Compliance] section of "
        f"{CONFIG_PATH}: {', '.join(missing_keys)}"
    )

    expected_values = {"gdpr": "true", "hipaa": "false"}
    wrong_values = {
        k: (compliance[k], expected_values[k])
        for k in expected_values
        if compliance[k] != expected_values[k]
    }
    assert not wrong_values, (
        "Unexpected value(s) in [Compliance] section:\n"
        + "\n".join(
            f"  {k}: expected '{exp}', found '{got}'"
            for k, (got, exp) in wrong_values.items()
        )
    )


def test_audit_log_not_present_yet():
    """
    The audit log should **not** exist before the student runs their solution.
    Its presence would indicate a polluted starting state.
    """
    assert not AUDIT_LOG_PATH.exists(), (
        f"The audit log {AUDIT_LOG_PATH} already exists, "
        "but it should be created by the student's work."
    )