# test_initial_state.py
#
# This test-suite validates that the staging host is still in the **initial**
# state before the student begins the “firewall-tuning script” exercise.
#
# WHAT WE CHECK FOR:
#   • The target directory /home/user/observability/firewall/ either does not
#     exist or, if it does exist, contains neither of the files the student
#     will be asked to create.
#   • The two required files *must NOT* be present yet:
#       - /home/user/observability/firewall/firewall_commands.sh
#       - /home/user/observability/firewall/firewall_rules.log
#
# If any of these resources already exist, the test will fail with a clear
# message so the environment can be reset before grading.

import os
import stat
import pytest

BASE_DIR = "/home/user/observability/firewall"
COMMANDS_PATH = os.path.join(BASE_DIR, "firewall_commands.sh")
RULES_PATH = os.path.join(BASE_DIR, "firewall_rules.log")


def _describe_path(path: str) -> str:
    """
    Helper: return a human-readable description of what *is* at `path`
    so failure messages are informative.
    """
    if not os.path.exists(path):
        return "does not exist"
    if os.path.isdir(path):
        return "is a directory"
    if os.path.islink(path):
        return "is a symlink"
    mode = oct(stat.S_IMODE(os.lstat(path).st_mode))
    return f"is a file (mode {mode})"


@pytest.mark.parametrize(
    "target_path, description",
    [
        (COMMANDS_PATH, "firewall commands script"),
        (RULES_PATH, "firewall rules log"),
    ],
)
def test_required_files_do_not_exist_yet(target_path: str, description: str):
    """
    BEFORE the student starts, the two expected files must be completely absent.
    We deliberately *fail* if anything already occupies their paths, including
    files, directories, symlinks, sockets, etc.
    """
    assert not os.path.exists(
        target_path
    ), (
        f"The {description} should not exist yet at {target_path}, "
        f"but {_describe_path(target_path)}."
    )


def test_firewall_directory_is_clean_or_absent():
    """
    The parent directory may or may not exist.  If it exists, it must not
    contain either of the target filenames; this guards against stale files
    from previous runs.
    """
    if not os.path.exists(BASE_DIR):
        pytest.skip(f"{BASE_DIR} does not exist yet (this is expected).")

    # Directory exists — enumerate its contents defensively.
    offending_items = [
        item
        for item in (COMMANDS_PATH, RULES_PATH)
        if os.path.exists(item)
    ]
    assert (
        not offending_items
    ), (
        f"The following items already exist in {BASE_DIR} but should not: "
        f"{', '.join(offending_items)}"
    )