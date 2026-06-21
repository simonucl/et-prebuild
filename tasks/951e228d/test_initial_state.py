# test_initial_state.py
#
# Pytest suite to validate the **initial** filesystem state for
# the “tiny firewall” exercise *before* the student performs any action.
#
# What we assert:
# 1. The firewall directory “/home/user/firewall” exists and is a directory.
# 2. The file “/home/user/firewall/rules.conf” exists, is writable,
#    and its exact byte-content is two characters:  "#\n".
# 3. No other files or directories exist inside “/home/user/firewall”.
#
# We explicitly do NOT look for (or mention) any of the files that are
# expected to be created *after* the student completes the task, in
# compliance with the autograder guidelines.

import os
from pathlib import Path

import pytest

FIREWALL_DIR = Path("/home/user/firewall")
RULES_CONF = FIREWALL_DIR / "rules.conf"


def test_firewall_directory_exists_and_is_directory():
    assert FIREWALL_DIR.exists(), (
        f"Expected firewall directory {FIREWALL_DIR} to exist, "
        "but it is missing."
    )
    assert FIREWALL_DIR.is_dir(), (
        f"{FIREWALL_DIR} exists but is not a directory."
    )
    # Directory should be writable by current user
    assert os.access(FIREWALL_DIR, os.W_OK), (
        f"Firewall directory {FIREWALL_DIR} is not writable by the current user."
    )


def test_rules_conf_exists_with_correct_content_and_permissions():
    assert RULES_CONF.exists(), (
        f"Expected rules file {RULES_CONF} to exist inside {FIREWALL_DIR}, "
        "but it is missing."
    )
    assert RULES_CONF.is_file(), f"{RULES_CONF} exists but is not a regular file."

    # File should be writable by current user
    assert os.access(RULES_CONF, os.W_OK), (
        f"Rules file {RULES_CONF} is not writable by the current user."
    )

    # Content must be exactly "#\n" (hash followed by newline), no more, no less
    content = RULES_CONF.read_bytes()
    expected = b"#\n"
    assert content == expected, (
        f"{RULES_CONF} content is incorrect.\n"
        f"Expected exact bytes: {expected!r}\n"
        f"Actual bytes:   {content!r}"
    )


def test_no_extra_files_in_firewall_directory():
    # Only "rules.conf" should be present at this point
    entries = [p.name for p in FIREWALL_DIR.iterdir()]
    extra_entries = sorted(set(entries) - {"rules.conf"})
    assert not extra_entries, (
        f"Unexpected files or directories found in {FIREWALL_DIR}: {extra_entries}. "
        "The directory is expected to contain only 'rules.conf' at the start."
    )