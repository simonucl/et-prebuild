# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student begins the localisation-sync task.
#
# It checks that:
#   • The English master file exists and already contains the five expected
#     keys (in order) in its [CORE] section.
#   • The French translation file exists and currently contains only the
#     three original keys (and is missing the two new ones).
#   • No update_log.txt file is present yet.
#
# The tests purposefully fail with a clear message if any pre-condition is
# violated.
#
# Only stdlib + pytest are used.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
LOCALE_DIR = PROJECT_DIR / "locale"

EN_FILE = LOCALE_DIR / "en_US.ini"
FR_FILE = LOCALE_DIR / "fr_FR.ini"
LOG_FILE = PROJECT_DIR / "update_log.txt"

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def extract_core_keys(path: Path):
    """
    Return a list of (key, value) pairs that appear *inside* the [CORE] section
    of the given .ini file, in the exact textual order they occur.

    Lines with no '=' sign and blank / comment lines are ignored.
    """
    keys = []
    in_core = False
    with path.open(encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith(";") or line.startswith("#"):
                continue  # ignore empty or comment lines
            if line.startswith("[") and line.endswith("]"):
                in_core = line.lower() == "[core]"
                continue

            if in_core and "=" in line:
                key, _, value = line.partition("=")
                keys.append((key.strip(), value.strip()))
            elif in_core and "[" in line and "]" in line:
                # Another section started → break once we leave [CORE]
                break
    return keys

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_file_presence():
    """Verify that the expected initial files exist (and nothing extra)."""
    assert EN_FILE.is_file(), (
        "Missing English master file at "
        f"{EN_FILE}.  It must be present before you start the task."
    )
    assert FR_FILE.is_file(), (
        "Missing French translation file at "
        f"{FR_FILE}.  It must be present before you start the task."
    )
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but it should not be present in the "
        "initial state. It will be created by the student script."
    )


def test_english_master_contents():
    """The master file must already have the full, updated key set."""
    expected_order = [
        "greeting",
        "farewell",
        "prompt",
        "thanks",
        "error_message",
    ]
    core_pairs = extract_core_keys(EN_FILE)
    found_keys = [k for k, _ in core_pairs]

    assert found_keys, (
        "Section [CORE] was not found or contained no keys in "
        f"{EN_FILE}"
    )

    assert found_keys == expected_order, (
        f"{EN_FILE} does not contain the expected keys in the correct order.\n"
        f"Expected order: {expected_order}\n"
        f"Found order:    {found_keys}"
    )


def test_french_translation_contents():
    """
    The French file must NOT yet contain the two new keys, but must
    contain the three original ones in the correct order.
    """
    expected_initial_order = ["greeting", "farewell", "prompt"]
    forbidden_keys = {"thanks", "error_message"}

    core_pairs = extract_core_keys(FR_FILE)
    found_keys = [k for k, _ in core_pairs]

    assert found_keys == expected_initial_order, (
        f"{FR_FILE} should initially contain only the keys "
        f"{expected_initial_order} (in that exact order).\n"
        f"Currently found keys: {found_keys}"
    )

    forbidden_present = [k for k in found_keys if k in forbidden_keys]
    assert not forbidden_present, (
        f"The keys {forbidden_present} should NOT yet be present in "
        f"{FR_FILE}. They will be added by the student."
    )