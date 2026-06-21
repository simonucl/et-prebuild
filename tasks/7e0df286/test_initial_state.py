# test_initial_state.py
#
# This pytest suite verifies that the workspace starts from the
# expected, pristine state.  It checks ONLY the resources that must
# already exist before the student carries out any steps:
#
#   1. Directory: /home/user/project/api_service
#   2. File:      /home/user/project/api_service/config.ini
#
# Do NOT add tests for the output artefacts that the student is
# supposed to create later (e.g. config_summary.log).

import os
import textwrap
from pathlib import Path

# ----------------------------------------------------------------------
# Canonical content of /home/user/project/api_service/config.ini
# The string below MUST match byte-for-byte, including all blank lines
# and the single trailing newline at the very end.
# ----------------------------------------------------------------------
EXPECTED_INI_CONTENT = textwrap.dedent(
    """\
    [Database]
    host=localhost
    port=5432
    user=dbuser
    password=secret

    [API]
    base_url=https://api.example.com
    timeout=30
    retries=3

    [Caching]
    enabled=true
    ttl=600
    """
)

API_SERVICE_DIR = Path("/home/user/project/api_service")
CONFIG_INI_PATH = API_SERVICE_DIR / "config.ini"


def test_api_service_directory_exists():
    """The /home/user/project/api_service directory must already exist."""
    assert API_SERVICE_DIR.is_dir(), (
        f"Required directory is missing: {API_SERVICE_DIR}. "
        "Ensure the project was unpacked correctly."
    )


def test_config_ini_exists():
    """The config.ini file must already be present inside api_service/."""
    assert CONFIG_INI_PATH.is_file(), (
        f"Required file is missing: {CONFIG_INI_PATH}. "
        "The starting workspace is incomplete."
    )


def test_config_ini_content_is_pristine():
    """
    The initial config.ini file must be in its pristine state—exactly the
    same bytes as specified in the task description.
    """
    with CONFIG_INI_PATH.open(encoding="utf-8") as fh:
        actual_content = fh.read()

    assert actual_content == EXPECTED_INI_CONTENT, (
        "The content of config.ini differs from the expected baseline.\n"
        "Please restore the original file so the exercise starts from a "
        "known good state."
    )