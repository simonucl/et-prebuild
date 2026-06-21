# test_initial_state.py
#
# This test-suite verifies the filesystem state *before* the student
# performs any actions.  It intentionally avoids looking for any
# files that are supposed to be created by the task itself.
#
# Preconditions we assert:
#   • Directories /home/user/configs and /home/user/change_logs exist.
#   • The legacy configuration file exists at
#       /home/user/configs/legacy.conf
#   • The file is *not* valid UTF-8 but *is* valid ISO-8859-1
#     (a.k.a. latin-1) and contains expected sample phrases.

import os
import pytest


CONFIG_DIR = "/home/user/configs"
CHANGE_LOG_DIR = "/home/user/change_logs"
LEGACY_CONF = os.path.join(CONFIG_DIR, "legacy.conf")


def test_configs_directory_exists():
    assert os.path.isdir(CONFIG_DIR), (
        f"Required directory {CONFIG_DIR!r} is missing."
    )


def test_change_logs_directory_exists():
    assert os.path.isdir(CHANGE_LOG_DIR), (
        f"Required directory {CHANGE_LOG_DIR!r} is missing."
    )


def test_legacy_conf_exists():
    assert os.path.isfile(LEGACY_CONF), (
        f"Legacy configuration file {LEGACY_CONF!r} is missing."
    )


def test_legacy_conf_encoding_iso_8859_1():
    """
    Ensure the legacy configuration file is *not* UTF-8 but *is*
    decodable as ISO-8859-1 and contains known reference text.
    """
    with open(LEGACY_CONF, "rb") as fh:
        raw = fh.read()

    # It should raise an error when treated as UTF-8
    with pytest.raises(UnicodeDecodeError):
        raw.decode("utf-8")

    # It must cleanly decode as ISO-8859-1 and contain expected text.
    text = raw.decode("latin-1")  # latin-1 == ISO-8859-1
    expected_phrase = "Bem-vindo ao café!"
    assert expected_phrase in text, (
        f"The file did not decode as ISO-8859-1 or is missing the expected "
        f"phrase {expected_phrase!r}."
    )