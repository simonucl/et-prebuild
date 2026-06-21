# test_initial_state.py
#
# This test-suite verifies the *initial* state of the filesystem before the
# student performs any action.  It checks only the pre-existing resources
# (input files/directories) and purposefully ignores any artefacts that the
# student is expected to create later.
#
# Rules complied with:
#   • Uses only stdlib + pytest.
#   • Uses absolute paths.
#   • Does NOT test for any output files (e.g. change_audit.log).

import os
import stat
import pytest

HOME = "/home/user"
CONFIG_DIR = os.path.join(HOME, "configs")
WEBSERVER_CONF = os.path.join(CONFIG_DIR, "webserver.conf")


def test_config_directory_exists_and_permissions():
    assert os.path.isdir(CONFIG_DIR), (
        f"Expected directory {CONFIG_DIR!r} to exist."
    )

    st = os.stat(CONFIG_DIR)
    mode = stat.S_IMODE(st.st_mode)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory {CONFIG_DIR!r} should have permissions "
        f"{oct(expected_mode)}, but has {oct(mode)}."
    )


def test_webserver_conf_exists_and_permissions():
    assert os.path.isfile(WEBSERVER_CONF), (
        f"Expected config file {WEBSERVER_CONF!r} to exist."
    )

    st = os.stat(WEBSERVER_CONF)
    mode = stat.S_IMODE(st.st_mode)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"File {WEBSERVER_CONF!r} should have permissions "
        f"{oct(expected_mode)}, but has {oct(mode)}."
    )


def test_webserver_conf_initial_content():
    expected_lines = [
        "# Web Server Configuration\n",
        "ENABLE_LOGS=false\n",
        "MAX_USERS=50\n",
        "PORT=8080\n",
        "TIMEZONE=UTC\n",
    ]

    with open(WEBSERVER_CONF, "r", encoding="utf-8") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, (
        f"Initial content of {WEBSERVER_CONF!r} is incorrect.\n"
        f"Expected:\n{''.join(expected_lines)}\n"
        f"Found:\n{''.join(actual_lines)}"
    )