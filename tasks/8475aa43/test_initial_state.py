# test_initial_state.py
#
# This pytest suite validates that the machine is in a **clean, pre-provisioning**
# state *before* the student runs their commands.  None of the target artefacts
# (/home/user/provisioning, prod.env, setup.log) should exist yet.  If any of
# them are present the test will explain exactly what needs to be removed so
# that the student can start from a known good baseline.
#
# NOTE:  Only the Python standard library and pytest are used here.

import os
import stat
import re
from pathlib import Path

PROV_DIR = Path("/home/user/provisioning")
ENV_FILE = PROV_DIR / "prod.env"
LOG_FILE = PROV_DIR / "setup.log"

ENV_EXPECTED_CONTENT = "API_TOKEN=prod-123456\nREGION=us-east-2\n"
ENV_EXPECTED_MODE = 0o600
LOG_EXPECTED_REGEX = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} prod\.env configured$"
)


def _file_mode(path: Path) -> int:
    """Return the file mode bits (e.g. 0o644)."""
    return stat.S_IMODE(path.stat().st_mode)


def test_provisioning_directory_absent_or_empty():
    """
    The provisioning directory should **not yet be populated**.

    Acceptable initial states:
      • Directory is completely absent (preferred / expected).
      • Directory exists but is totally empty.

    Any existing content would indicate that the machine is already
    provisioned (in whole or in part) and should be cleared before the
    student begins the exercise.
    """
    if not PROV_DIR.exists():
        # Ideal clean-slate scenario — nothing to check further.
        return

    # Directory exists – make sure it's sane and empty.
    assert PROV_DIR.is_dir(), (
        f"'{PROV_DIR}' exists but is not a directory. "
        "Remove or rename it before starting the provisioning task."
    )

    contents = list(PROV_DIR.iterdir())
    assert (
        len(contents) == 0
    ), (
        f"'{PROV_DIR}' already contains files/directories: "
        f"{', '.join(p.name for p in contents)}. "
        "Start from an empty directory or remove it entirely."
    )


def test_prod_env_file_absent():
    """
    The prod.env file must **not** exist prior to the student's actions.
    """
    assert not ENV_FILE.exists(), (
        f"The file '{ENV_FILE}' already exists. The exercise expects the "
        "student to create it from scratch."
    )


def test_setup_log_file_absent():
    """
    The setup.log file must **not** exist prior to the student's actions.
    """
    assert not LOG_FILE.exists(), (
        f"The file '{LOG_FILE}' already exists. The exercise expects the "
        "student to create it from scratch."
    )