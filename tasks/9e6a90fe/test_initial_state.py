# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the workstation
# before the student performs any action.  Nothing that the assignment
# asks the student to create should exist yet.

import os
from pathlib import Path
import stat
import pytest

# Absolute paths that must be absent at the very beginning
HOME = Path("/home/user")
PRIVATE_KEY = HOME / "alert_key"
PUBLIC_KEY = HOME / "alert_key.pub"
SETUP_DIR = HOME / "ssh_setup"
LOG_FILE = SETUP_DIR / "setup.log"

@pytest.mark.parametrize(
    "path_obj, description",
    [
        (PRIVATE_KEY, "private key"),
        (PUBLIC_KEY, "public key"),
        (LOG_FILE, "log file"),
        (SETUP_DIR, "setup directory"),
    ],
)
def test_absence_of_expected_artifacts(path_obj: Path, description: str):
    """
    Ensure none of the files/directories that the student is supposed to
    create are present before they start the task.
    """
    assert not path_obj.exists(), (
        f"The {description} ({path_obj}) already exists. "
        "The workstation must start in a pristine state."
    )


def test_no_other_ed25519_key_named_alert_key():
    """
    Guard against an edge-case where the user might have an SSH public
    key with the comment 'alert_key' lying around elsewhere in $HOME.
    """
    suspicious_keys = []

    for root, _dirs, files in os.walk(HOME):
        for fname in files:
            if fname.endswith(".pub"):
                full_path = Path(root) / fname
                try:
                    with full_path.open("r", encoding="utf-8") as fp:
                        contents = fp.readline().strip()
                    if contents.endswith(" alert_key"):
                        suspicious_keys.append(full_path)
                except (UnicodeDecodeError, PermissionError):
                    # If we can't read it, ignore—it can't be a valid candidate anyhow
                    continue

    assert not suspicious_keys, (
        "Found unexpected SSH public key(s) that already carry the comment "
        "'alert_key':\n"
        + "\n".join(map(str, suspicious_keys))
        + "\nRemove these keys so the exercise starts from a clean slate."
    )


def _mode_bits(path_obj: Path) -> int:
    """Return the permission bits of a path, or 0 if it does not exist."""
    try:
        return stat.S_IMODE(path_obj.stat().st_mode)
    except FileNotFoundError:
        return 0


@pytest.mark.parametrize(
    "path_obj",
    [PRIVATE_KEY, PUBLIC_KEY, LOG_FILE],
)
def test_permissions_not_preconfigured(path_obj: Path):
    """
    If any of the target files somehow exist already (which they
    shouldn't), make sure they *don't* accidentally have the correct
    permissions.  Their very existence is already a failure, but this
    doubles as a safety check to catch mis-configured images.
    """
    mode = _mode_bits(path_obj)
    assert mode not in (0o600, 0o644), (
        f"The path {path_obj} unexpectedly has permission {oct(mode)}. "
        "The workstation must start without pre-configured artefacts."
    )