# test_initial_state.py
#
# This pytest suite validates that the filesystem is in the expected
# “before-the-student-does-anything” state for the SSH key-generation
# assignment.  At this point none of the deliverable artefacts should
# exist yet.  If any of them are already present the test will fail
# with an explanatory message.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
SSH_DIR = os.path.join(HOME, ".ssh")
DIAG_DIR = os.path.join(HOME, "diagnostics")

PRIVATE_KEY = os.path.join(SSH_DIR, "support_eng_key")
PUBLIC_KEY = PRIVATE_KEY + ".pub"
AUTHORIZED_KEYS = os.path.join(SSH_DIR, "authorized_keys")
LOG_FILE = os.path.join(DIAG_DIR, "ssh_collection.log")


@pytest.mark.parametrize(
    "path, kind",
    [
        (PRIVATE_KEY, "private key"),
        (PUBLIC_KEY, "public key"),
        (LOG_FILE, "diagnostic log"),
    ],
)
def test_target_files_do_not_exist_yet(path, kind):
    """
    Before the exercise starts the student-generated files must **not**
    be present.  Having them in place would indicate that the lab VM
    is not in the pristine state expected by the grader.
    """
    assert not os.path.exists(path), (
        f"The {kind} file '{path}' already exists before the student "
        f"has had a chance to create it.  Please reset the environment "
        f"to a clean state."
    )


def test_authorized_keys_is_clean_of_new_entry():
    """
    The student will *append* their freshly generated public key line to
    authorized_keys.  Prior to the exercise we only check that the file
    (if it exists at all) is not a dangling symlink and is a plain file.
    We do **not** enforce its absence because a real user may legitimately
    have pre-existing keys for other purposes.
    """
    if os.path.exists(AUTHORIZED_KEYS):
        # It must be a regular file, not a directory or device.
        st = os.lstat(AUTHORIZED_KEYS)
        assert stat.S_ISREG(st.st_mode), (
            f"'{AUTHORIZED_KEYS}' exists but is not a regular file "
            f"(mode: {oct(st.st_mode & 0o170000)}).  "
            f"Please fix or remove it before starting the task."
        )


def test_no_leftover_artifacts_in_target_directories():
    """
    Ensure the .ssh and diagnostics directories (if they exist) do not
    already contain files produced by a previous run of the assignment.
    We whitelist common default files (e.g. 'known_hosts').
    """
    leftover_files = []

    if os.path.isdir(SSH_DIR):
        for fname in os.listdir(SSH_DIR):
            if fname.startswith("support_eng_key"):
                leftover_files.append(os.path.join(SSH_DIR, fname))

    if os.path.isdir(DIAG_DIR):
        for fname in os.listdir(DIAG_DIR):
            if fname == "ssh_collection.log":
                leftover_files.append(os.path.join(DIAG_DIR, fname))

    assert not leftover_files, (
        "Found unexpected assignment-related files that should not exist "
        f"yet:\n  - " + "\n  - ".join(leftover_files) +
        "\nReset the workspace before running the task."
    )