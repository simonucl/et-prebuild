# test_initial_state.py
#
# This pytest suite validates the filesystem **before** the student
# starts working on the task “Apply a configuration patch and record the outcome”.
#
# The checks make sure that only the *initial* prerequisites are present
# and that none of the artefacts the student must create already exist.
#
# • Uses only the Python stdlib + pytest.
# • All paths are absolute, rooted at /home/user.
#
# If any assertion fails the accompanying message will
# explain exactly what is wrong with the starting state.

import pathlib
import pytest


HOME = pathlib.Path("/home/user")

WEBAPP_DIR   = HOME / "webapp"
PATCHES_DIR  = HOME / "patches"
LOG_DIR      = HOME / "patch_logs"

CONFIG_FILE  = WEBAPP_DIR / "settings.conf"
PATCH_FILE   = PATCHES_DIR / "settings.patch"

BACKUP_FILE  = WEBAPP_DIR / "settings.conf.bak"
LOG_FILE     = LOG_DIR   / "apply_settings_patch.log"


def test_required_directories_exist():
    assert WEBAPP_DIR.is_dir(), f"Missing directory: {WEBAPP_DIR}"
    assert PATCHES_DIR.is_dir(), f"Missing directory: {PATCHES_DIR}"


def test_required_files_exist():
    assert CONFIG_FILE.is_file(), f"Missing configuration file: {CONFIG_FILE}"
    assert PATCH_FILE.is_file(), f"Missing patch file: {PATCH_FILE}"


def test_no_student_outputs_pre_exist():
    assert not BACKUP_FILE.exists(), (
        f"Backup file already exists: {BACKUP_FILE} (should be created by the student)"
    )
    assert not LOG_FILE.exists(), (
        f"Log file already exists: {LOG_FILE} (should be created by the student)"
    )


def test_settings_conf_is_unpatched():
    """
    The original configuration must still be the *old* version:
      • PORT must be 8080, not 9090
      • DEBUG must be false, not true
      • MAX_CONNECTIONS must be absent
    """
    content = CONFIG_FILE.read_text(encoding="utf-8").splitlines()

    # Positive expectations (must be present)
    assert any(line.strip() == "PORT=8080" for line in content), (
        f"{CONFIG_FILE} should contain 'PORT=8080' before the patch is applied."
    )
    assert any(line.strip() == "DEBUG=false" for line in content), (
        f"{CONFIG_FILE} should contain 'DEBUG=false' before the patch is applied."
    )

    # Negative expectations (must NOT be present yet)
    forbidden_snippets = ("PORT=9090", "DEBUG=true", "MAX_CONNECTIONS=100")
    for snippet in forbidden_snippets:
        assert all(snippet not in line for line in content), (
            f"{CONFIG_FILE} already contains '{snippet}', "
            "but it should only appear after the patch is applied."
        )