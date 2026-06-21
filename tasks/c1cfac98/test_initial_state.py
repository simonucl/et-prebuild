# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before**
# any credential-rotation action is performed.  If one of these tests
# fails it means the starting point is not what the assignment expects,
# so the student’s one-liner will not be judged fairly.

import os
from pathlib import Path
import pytest

# ---------- Constants ---------- #
CONFIG_YAML = Path("/home/user/app/config.yaml")
SECRET_TOML = Path("/home/user/app/secret.toml")
LOG_DIR     = Path("/home/user/logs")
LOG_FILE    = LOG_DIR / "cred_rotation.log"


# ---------- Helper utilities ---------- #
def read_file_lines(path: Path):
    """Return a list of lines (stripped of trailing newlines) from *path*."""
    return path.read_text(encoding="utf-8").splitlines()


# ---------- Tests ---------- #
def test_config_yaml_initial_state():
    """`config.yaml` must exist and still contain the old password."""
    assert CONFIG_YAML.is_file(), (
        f"Expected YAML config file at '{CONFIG_YAML}', but it is missing."
    )

    lines = read_file_lines(CONFIG_YAML)

    # Presence of key content
    assert any(line.strip() == "database:" for line in lines), (
        f"'{CONFIG_YAML}' should contain a 'database:' section."
    )
    assert any(line.strip() == "user: appuser" for line in lines), (
        f"'{CONFIG_YAML}' should have the line 'user: appuser' in its initial state."
    )
    assert any(line.strip() == "password: changeme123" for line in lines), (
        f"'{CONFIG_YAML}' should have the line 'password: changeme123' in its initial state."
    )

    # Absence of new secret
    file_text = "\n".join(lines)
    assert "S3cur3P@ssw0rd!" not in file_text, (
        f"Rotated password found in '{CONFIG_YAML}', "
        "but credentials should not be rotated yet."
    )


def test_secret_toml_initial_state():
    """`secret.toml` must exist and still contain the old token."""
    assert SECRET_TOML.is_file(), (
        f"Expected TOML secret file at '{SECRET_TOML}', but it is missing."
    )

    lines = read_file_lines(SECRET_TOML)

    # Presence of key content
    assert any(line.strip() == "[api]" for line in lines), (
        f"'{SECRET_TOML}' should contain an '[api]' table."
    )
    assert any(line.strip() == 'token = "changeme123"' for line in lines), (
        f"'{SECRET_TOML}' should have the line 'token = \"changeme123\"' in its initial state."
    )

    # Absence of new secret
    file_text = "\n".join(lines)
    assert "S3cur3Tok3n!" not in file_text, (
        f"Rotated token found in '{SECRET_TOML}', "
        "but credentials should not be rotated yet."
    )


def test_log_directory_and_absence_of_rotation_log():
    """
    The `/home/user/logs` directory must exist and be writable,
    and `cred_rotation.log` must *not* exist yet.
    """
    assert LOG_DIR.is_dir(), (
        f"Expected log directory at '{LOG_DIR}', but it is missing or not a directory."
    )
    assert os.access(LOG_DIR, os.W_OK), (
        f"Log directory '{LOG_DIR}' is not writable by the current user."
    )
    assert not LOG_FILE.exists(), (
        f"'{LOG_FILE}' should NOT exist before credential rotation has occurred."
    )