# test_initial_state.py
#
# This pytest file asserts that none of the delivery artefacts for the
# “edge-computing IoT gateway firewall” task are present **before** the
# student starts working.  If any of the required paths already exist,
# the test will fail with a clear, actionable message.

from pathlib import Path
import os
import stat
import pytest

BASE_DIR = Path("/home/user/deployment/firewall")
SCRIPT = BASE_DIR / "iot_firewall_rules.sh"
README = BASE_DIR / "README_FIREWALL.txt"
LOG    = BASE_DIR / "setup.log"


def _format_perm(bits: int) -> str:
    """Return permissions in octal string form, e.g. '0755'."""
    return format(bits & 0o7777, "04o")


@pytest.mark.parametrize(
    "path, should_exist",
    [
        (BASE_DIR, False),          # Directory must NOT exist yet
        (SCRIPT,   False),          # Script must NOT exist yet
        (README,   False),          # README must NOT exist yet
        (LOG,      False),          # Log file must NOT exist yet
    ],
)
def test_paths_absent(path: Path, should_exist: bool):
    """
    Ensure the directory tree and files that the student has to create
    do NOT exist at the beginning of the exercise.
    """
    if should_exist:
        assert path.exists(), f"Expected {path} to exist, but it is missing."
    else:
        assert not path.exists(), (
            f"{path} already exists — the initial state must be clean. "
            "Remove it before beginning the task."
        )


def test_no_leftover_permissions():
    """
    If anything under /home/user/deployment exists already for some
    unexpected reason, make sure there are no accidentally executable
    firewall scripts lying around.  This guards against a polluted
    workspace.  If the base directory is absent (the normal case), the
    test is skipped.
    """
    if not BASE_DIR.exists():
        pytest.skip("Base directory does not exist; workspace is clean.")

    # Walk the tree defensively and flag any executable regular files.
    for file_path in BASE_DIR.rglob("*"):
        if file_path.is_file():
            mode = file_path.stat().st_mode
            if mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                perms = _format_perm(mode)
                pytest.fail(
                    f"Found unexpected executable file {file_path} "
                    f"with permissions {_format_perm(mode)}; "
                    "the initial workspace must not contain executables."
                )