# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student starts working on the SSH-key-rotation task.
#
# The tests assert that:
#   • /home/user/.ssh exists with permission 0700.
#   • /home/user/.ssh/authorized_keys exists with permission 0600 and contains
#     exactly the two expected lines (plus a single trailing newline).
#   • No other files are present inside /home/user/.ssh.
#   • The key-pair files that will be created later do **not** exist yet.
#   • /home/user/rotation_logs does **not** exist yet.

import os
import stat
import pytest

HOME = "/home/user"
SSH_DIR = os.path.join(HOME, ".ssh")
AUTHORIZED_KEYS = os.path.join(SSH_DIR, "authorized_keys")
NEW_PRIV_KEY = os.path.join(SSH_DIR, "id_ed25519_rotate")
NEW_PUB_KEY = NEW_PRIV_KEY + ".pub"
ROTATION_LOG_DIR = os.path.join(HOME, "rotation_logs")

EXPECTED_LINE_1 = (
    "ssh-ed25519 "
    "AAAAC3NzaC1lZDI1NTE5AAAAIDSgcf5xgxN0R8vG5YkNVrYJv1nVbWcv1O3MH8b6XAQ1 "
    "old-key-2023"
)
EXPECTED_LINE_2 = (
    "ssh-rsa "
    "AAAAB3NzaC1yc2EAAAADAQABAAABAQC4an1j2xy7b3Dx3XcX8GpXxFfXriYrAYx0QHoQOH9d6Qhvz"
    "XnYFho7ozatajIuHQw6mbeid8X8oI6INBnNw+9xCLdfDUbqMf95xTeNwCvufqJgHE4vvAJ8Njgr"
    "ZpTr6lYQkPzwHC27bMqf+AKeFEg3UhYg2uscd/lXFk4Isllwz6TQ1iXwRXy2U1UXoCM "
    "deployment-key"
)


def _mode(path):
    """Return the permission bits (e.g. 0o600) for the given path."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_ssh_directory_exists_with_correct_permissions():
    assert os.path.isdir(SSH_DIR), f"Directory {SSH_DIR} is missing."
    perms = _mode(SSH_DIR)
    assert perms == 0o700, (
        f"Directory {SSH_DIR} should have mode 700, found {oct(perms)}."
    )


def test_authorized_keys_exists_and_has_correct_permissions():
    assert os.path.isfile(AUTHORIZED_KEYS), (
        f"File {AUTHORIZED_KEYS} is missing."
    )
    perms = _mode(AUTHORIZED_KEYS)
    assert perms == 0o600, (
        f"File {AUTHORIZED_KEYS} should have mode 600, found {oct(perms)}."
    )


def test_authorized_keys_contains_exact_two_expected_lines():
    with open(AUTHORIZED_KEYS, "r", encoding="utf-8") as fh:
        content = fh.read()

    # Ensure exactly one trailing newline and not two.
    assert content.endswith(
        "\n"
    ) and not content.endswith(
        "\n\n"
    ), f"{AUTHORIZED_KEYS} must end with exactly one trailing newline."

    lines = content.rstrip("\n").split("\n")
    assert len(lines) == 2, (
        f"{AUTHORIZED_KEYS} must contain exactly 2 lines before work starts; "
        f"found {len(lines)} line(s)."
    )
    assert lines[0] == EXPECTED_LINE_1, (
        "First line of authorized_keys does not match expected old key.\n"
        f"Expected: {EXPECTED_LINE_1}\nFound:    {lines[0]}"
    )
    assert lines[1] == EXPECTED_LINE_2, (
        "Second line of authorized_keys does not match expected deployment key.\n"
        f"Expected: {EXPECTED_LINE_2}\nFound:    {lines[1]}"
    )


def test_no_other_files_present_in_ssh_directory():
    items = [f for f in os.listdir(SSH_DIR) if not f.startswith(".")]
    assert items == [
        "authorized_keys"
    ], (
        f"{SSH_DIR} should contain only 'authorized_keys' before the task starts. "
        f"Found extra items: {set(items) - {'authorized_keys'}}"
    )


def test_new_keypair_files_do_not_exist_yet():
    assert not os.path.exists(
        NEW_PRIV_KEY
    ), f"Private key {NEW_PRIV_KEY} should not exist before rotation begins."
    assert not os.path.exists(
        NEW_PUB_KEY
    ), f"Public key {NEW_PUB_KEY} should not exist before rotation begins."


def test_rotation_log_directory_does_not_exist_yet():
    assert not os.path.exists(
        ROTATION_LOG_DIR
    ), f"Directory {ROTATION_LOG_DIR} should not exist before rotation begins."