# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state
# *before* the student starts working on the IoT-gateway task.
#
# It checks only the resources that are expected to be present
# in the baseline image.  It deliberately ignores (and therefore
# does NOT mention) any artefacts that the student will create
# later (.env, deploy.sh, deployment.log, .gitignore, …).
#
# If any of these tests fail, the starting image is corrupt and
# the assignment cannot be completed as specified.

import re
from pathlib import Path

import pytest

# Constants for paths used in the initial state checks
HOME           = Path("/home/user")
PROJECT_ROOT   = HOME / "projects" / "iot_gateway"
TEMPLATE_ENV   = PROJECT_ROOT / "config.template.env"
BASHRC         = HOME / ".bashrc"

# --------------------------------------------------------------------------- #
# Helper utilities                                                             #
# --------------------------------------------------------------------------- #

EXPECTED_PLACEHOLDER_LINES = [
    r"EDGE_DEVICE_ID=<DEV_ID>",
    r"MQTT_BROKER_HOST=<BROKER_HOST>",
    r"MQTT_BROKER_PORT=<BROKER_PORT>",
    r"SENSOR_POLL_INTERVAL=<POLL_INT>",
    r"FIRMWARE_VERSION=<FW_VER>",
]


def read_text_file(path: Path) -> str:
    """Return contents of *path* as text, raising a helpful assertion if unreadable."""
    assert path.exists(), f"Expected file at {path} to exist, but it is missing."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")  # Defensive failure


# --------------------------------------------------------------------------- #
# Tests                                                                        #
# --------------------------------------------------------------------------- #

def test_project_directory_exists():
    """The project root directory must be present."""
    assert PROJECT_ROOT.is_dir(), (
        f"Expected directory {PROJECT_ROOT} to exist, "
        "but it is missing or is not a directory."
    )


def test_template_env_exists_with_correct_placeholders():
    """
    Verify that config.template.env exists and contains the exact five placeholder
    lines (in order) that students are expected to turn into real values later.
    """
    content = read_text_file(TEMPLATE_ENV)
    # Split with universal newlines, strip trailing empty line if any
    lines = re.split(r"\r?\n", content.rstrip("\r\n"))
    assert lines == EXPECTED_PLACEHOLDER_LINES, (
        "The file config.template.env does not match the expected placeholder "
        "content.\n"
        f"Expected lines:\n{EXPECTED_PLACEHOLDER_LINES}\n\n"
        f"Actual lines:\n{lines}"
    )


def test_bashrc_exists_without_firmware_export():
    """
    The user's ~/.bashrc must already exist, but it should NOT yet contain the
    firmware export line that the student will add later.
    """
    bashrc_content = read_text_file(BASHRC)

    forbidden_line = 'export FIRMWARE_VERSION="v2.5.1" #edge_deploy'
    assert forbidden_line not in bashrc_content, (
        "The file ~/.bashrc already contains the firmware export line that the "
        "student is supposed to add later.  The starting image appears to be "
        "in an unexpected state."
    )