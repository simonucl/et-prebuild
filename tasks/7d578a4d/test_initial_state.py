# test_initial_state.py
#
# This test-suite validates that the system is in the EXPECTED *initial*
# configuration *before* the student makes any changes.  It checks that the
# two existing configuration files are present and still hold their original
# values.

import os
import re
import pytest

HOME = "/home/user"
OBS_DIR = os.path.join(HOME, "observability")

WATCHERS_PATH = os.path.join(OBS_DIR, "watchers.yaml")
GRAFANA_PATH = os.path.join(OBS_DIR, "grafana.toml")


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_text(path: str) -> str:
    """Read a text file using UTF-8 and return its contents."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# File-presence tests
# --------------------------------------------------------------------------- #
def test_observability_directory_exists():
    assert os.path.isdir(
        OBS_DIR
    ), f"Expected directory {OBS_DIR!r} to exist but it does not."


def test_watchers_file_exists():
    assert os.path.isfile(
        WATCHERS_PATH
    ), f"Expected file {WATCHERS_PATH!r} to exist but it does not."


def test_grafana_file_exists():
    assert os.path.isfile(
        GRAFANA_PATH
    ), f"Expected file {GRAFANA_PATH!r} to exist but it does not."


# --------------------------------------------------------------------------- #
# Content validation: watchers.yaml
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("metric", "expected_threshold", "unexpected_threshold"),
    [
        ("cpu_usage", 85, 80),
        ("memory_usage", 90, 88),
    ],
)
def test_watchers_thresholds(metric, expected_threshold, unexpected_threshold):
    """
    Verify that each metric in watchers.yaml still contains its ORIGINAL
    threshold value and has NOT yet been edited.
    """
    content = read_text(WATCHERS_PATH)

    # Regex to locate the metric block followed by a threshold value.
    # We use a tempered dotall search to stay within the block.
    pattern = (
        rf"{metric}:\s*?\n"  # the metric header
        rf"(?:[ \t].*?\n)*?"  # any number of indented lines
        rf"[ \t]*threshold:[ \t]*{expected_threshold}\b"
    )

    assert re.search(pattern, content, flags=re.IGNORECASE | re.MULTILINE), (
        f"{WATCHERS_PATH} does not contain the expected original threshold "
        f"value {expected_threshold} for {metric!r}.  Has it been modified?"
    )

    # Extra safety: ensure the file has not already been updated.
    assert str(unexpected_threshold) not in content, (
        f"{WATCHERS_PATH} already includes the value {unexpected_threshold} "
        f"for {metric!r}, but the task has not yet been performed."
    )


# --------------------------------------------------------------------------- #
# Content validation: grafana.toml
# --------------------------------------------------------------------------- #
def test_grafana_users_allow_sign_up_true():
    """
    The users.allow_sign_up flag should still be `true` in the initial state.
    """
    content = read_text(GRAFANA_PATH)
    assert re.search(
        r"^\s*allow_sign_up\s*=\s*true\s*$", content, flags=re.MULTILINE | re.IGNORECASE
    ), (
        f"{GRAFANA_PATH} should contain 'allow_sign_up = true' in its initial "
        f"state, but it does not."
    )
    # Ensure the value has not yet been flipped.
    assert not re.search(
        r"^\s*allow_sign_up\s*=\s*false\s*$", content, flags=re.MULTILINE | re.IGNORECASE
    ), (
        f"Found 'allow_sign_up = false' in {GRAFANA_PATH}, which indicates "
        f"the configuration has already been changed."
    )


def test_grafana_users_default_theme_light():
    """
    The users.default_theme should still be \"light\" in the initial state.
    """
    content = read_text(GRAFANA_PATH)
    assert re.search(
        r'^\s*default_theme\s*=\s*"light"\s*$', content, flags=re.MULTILINE | re.IGNORECASE
    ), (
        f"{GRAFANA_PATH} should contain 'default_theme = \"light\"' in its "
        f"initial state, but it does not."
    )
    # Guard against premature change.
    assert not re.search(
        r'^\s*default_theme\s*=\s*"dark"\s*$', content, flags=re.MULTILINE | re.IGNORECASE
    ), (
        f"Found 'default_theme = \"dark\"' in {GRAFANA_PATH}, which indicates "
        f"the configuration has already been changed."
    )