# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem is in the
# correct *initial* state **before** the student performs any action.
#
# What we assert:
#   1. /home/user/backup/config.yml exists and still contains the original
#      (unmodified) configuration.
#   2. /home/user/backup/job.toml exists and still contains the original
#      (unmodified) job definitions.
#
# What we deliberately do *NOT* assert:
#   • Any of the files / directories that are expected to be **created** by the
#     student (/home/user/backup/restore_test, restore_steps.log, …).  The
#     rubric explicitly forbids checking output artefacts in the initial-state
#     test.

from pathlib import Path
import sys
import pytest

CONFIG_YAML_PATH = Path("/home/user/backup/config.yml")
JOB_TOML_PATH = Path("/home/user/backup/job.toml")

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def normalize(text: str) -> str:
    """
    Strip leading/trailing blank lines and remove trailing whitespace on each
    line so that minor differences in trailing spaces do not break the test.
    """
    return "\n".join(line.rstrip() for line in text.strip().splitlines())

# --------------------------------------------------------------------------- #
# Expected ORIGINAL contents                                                  #
# --------------------------------------------------------------------------- #
EXPECTED_CONFIG_YAML = """
version: "1.0"
jobs:
  daily_backup:
    enabled: true
    source: /data
    destination: /backups/daily
    retention_days: 7
  restore_test:
    enabled: false
    source: /backups/daily/latest
    destination: /tmp/restore_test
    retention_days: 1
""".lstrip()

EXPECTED_JOB_TOML = """
[general]
log_level = "INFO"
threads = 2

[job.daily_backup]
cron = "0 2 * * *"
compression = "gzip"

[job.restore_test]
cron = ""
compression = "none"
""".lstrip()

# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_config_yaml_exists_and_is_unmodified():
    """The YAML configuration file must exist and remain unmodified."""
    assert CONFIG_YAML_PATH.exists(), (
        f"Expected YAML file '{CONFIG_YAML_PATH}' is missing."
    )

    file_content = CONFIG_YAML_PATH.read_text(encoding="utf-8")
    assert normalize(file_content) == normalize(EXPECTED_CONFIG_YAML), (
        "The contents of /home/user/backup/config.yml do not match the expected "
        "initial state.  Make sure the file has NOT been modified yet."
    )


def test_job_toml_exists_and_is_unmodified():
    """The TOML job definition file must exist and remain unmodified."""
    assert JOB_TOML_PATH.exists(), (
        f"Expected TOML file '{JOB_TOML_PATH}' is missing."
    )

    file_content = JOB_TOML_PATH.read_text(encoding="utf-8")
    assert normalize(file_content) == normalize(EXPECTED_JOB_TOML), (
        "The contents of /home/user/backup/job.toml do not match the expected "
        "initial state.  Make sure the file has NOT been modified yet."
    )