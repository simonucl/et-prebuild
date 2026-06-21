# test_initial_state.py
#
# This pytest suite verifies that the workstation is still in its
# pristine “before-the-exercise” state.  Nothing related to the
# forthcoming “audit_keys” task should be present yet.

import pytest
from pathlib import Path

HOME = Path("/home/user")
AUDIT_DIR = HOME / "audit_keys"

# Individual paths that must NOT exist yet
KEY_PRIVATE = AUDIT_DIR / "id_audit_rsa"
KEY_PUBLIC = AUDIT_DIR / "id_audit_rsa.pub"
LOG_CREATE = AUDIT_DIR / "key_creation.log"
LOG_PERMS = AUDIT_DIR / "permission_report.log"

SSH_DIR = HOME / ".ssh"
AUTHORIZED_KEYS = SSH_DIR / "authorized_keys"

ALL_AUDIT_PATHS = [
    AUDIT_DIR,
    KEY_PRIVATE,
    KEY_PUBLIC,
    LOG_CREATE,
    LOG_PERMS,
]


@pytest.mark.parametrize("path", ALL_AUDIT_PATHS)
def test_audit_paths_do_not_exist(path):
    """
    None of the audit-specific paths should exist yet.
    """
    assert not path.exists(), (
        f"{path} already exists, but it should NOT be present before "
        "you begin the exercise."
    )


def test_authorized_keys_does_not_yet_contain_comment():
    """
    If ~/.ssh/authorized_keys exists, it must not already include
    a key that ends with the required comment “audit@local”.
    """
    if not AUTHORIZED_KEYS.exists():
        pytest.skip("~/.ssh/authorized_keys does not exist yet – that is fine.")

    # Read file safely; restrict size in case the file is huge.
    # 5 MiB is generous for a text file containing public keys.
    max_size = 5 * 1024 * 1024
    assert AUTHORIZED_KEYS.stat().st_size <= max_size, (
        "~/.ssh/authorized_keys is unexpectedly large; aborting read."
    )

    content = AUTHORIZED_KEYS.read_text(encoding="utf-8", errors="replace")
    offending_lines = [
        line for line in content.splitlines() if line.strip().endswith("audit@local")
    ]
    assert (
        not offending_lines
    ), "The comment 'audit@local' is already present in ~/.ssh/authorized_keys."