# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student starts working on the “SSH-key installation &
# Kubernetes-Secret” exercise.
#
# It checks that only the pre-seeded artefacts are present and that none of the
# files the student is supposed to create already exist.

import os
import stat
import base64
import pytest

# --------------------------------------------------------------------------- #
# Constant paths                                                              #
# --------------------------------------------------------------------------- #
PRESEED_PRIV = "/home/user/preseed/id_ed25519"
PRESEED_PUB = "/home/user/preseed/id_ed25519.pub"

SSH_DIR = "/home/user/.ssh"
DEST_PRIV = f"{SSH_DIR}/id_ed25519"
DEST_PUB = f"{SSH_DIR}/id_ed25519.pub"
AUTH_KEYS = f"{SSH_DIR}/authorized_keys"

K8S_MANIFEST = "/home/user/k8s/operator/secret-ssh-key.yaml"
LOG_FILE = "/home/user/ssh_key_setup.log"

# --------------------------------------------------------------------------- #
# Expected contents of the two pre-seeded files                               #
# --------------------------------------------------------------------------- #
EXPECTED_PRIV_CONTENT = b"myprivatekey\n"
EXPECTED_PUB_CONTENT = (
    b"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIG15cHVibGlja2V5 user@training\n"
)

EXPECTED_BASE64 = "bXlwcml2YXRla2V5Cg=="  # base64 of "myprivatekey\n"


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def assert_mode(path: str, expected: int) -> None:
    """
    Assert that the numeric permission bits of `path` equal `expected`.
    (`expected` must be expressed as an octal such as 0o644.)
    """
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert (
        mode == expected
    ), f"{path!r} has mode {oct(mode)}, expected {oct(expected)}"


# --------------------------------------------------------------------------- #
# Tests for the pre-seeded files                                              #
# --------------------------------------------------------------------------- #
def test_preseed_private_key_exists_and_is_correct():
    assert os.path.isfile(
        PRESEED_PRIV
    ), f"Missing pre-seeded private key at {PRESEED_PRIV}"
    assert_mode(PRESEED_PRIV, 0o644)

    with open(PRESEED_PRIV, "rb") as fp:
        content = fp.read()
    assert (
        content == EXPECTED_PRIV_CONTENT
    ), "Pre-seeded private key content is not as expected"

    got_b64 = base64.b64encode(content).decode()
    assert (
        got_b64 == EXPECTED_BASE64
    ), "Base64 of pre-seeded private key is not the expected value"


def test_preseed_public_key_exists_and_is_correct():
    assert os.path.isfile(
        PRESEED_PUB
    ), f"Missing pre-seeded public key at {PRESEED_PUB}"
    assert_mode(PRESEED_PUB, 0o644)

    with open(PRESEED_PUB, "rb") as fp:
        content = fp.read()
    assert (
        content == EXPECTED_PUB_CONTENT
    ), "Pre-seeded public key content is not as expected"


# --------------------------------------------------------------------------- #
# Tests ensuring that post-task artefacts do NOT exist yet                    #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path",
    [
        SSH_DIR,
        DEST_PRIV,
        DEST_PUB,
        AUTH_KEYS,
        K8S_MANIFEST,
        LOG_FILE,
    ],
)
def test_student_targets_do_not_exist_yet(path):
    """
    None of the artefacts the student is supposed to create should exist
    at the initial state (with one caveat: ~/.ssh may already exist, and that
    is acceptable – we merely skip the existence assertion in that case).
    """
    # Special handling for ~/.ssh itself – it *may* exist.
    if path == SSH_DIR and os.path.isdir(path):
        # If the directory exists, check that the destination key files
        # inside of it are still absent.
        assert not os.path.exists(
            DEST_PRIV
        ), f"{DEST_PRIV} already exists; it should not before the task starts"
        assert not os.path.exists(
            DEST_PUB
        ), f"{DEST_PUB} already exists; it should not before the task starts"
        return

    assert not os.path.exists(
        path
    ), f"{path} already exists; it should not be present before the task starts"


def test_authorized_keys_does_not_contain_seed_pub_key():
    """
    If ~/.ssh/authorized_keys exists, it must NOT already contain the
    pre-seeded public-key line.  (Students are supposed to append it.)
    """
    if not os.path.isfile(AUTH_KEYS):
        pytest.skip("authorized_keys does not exist yet – OK (will be created)")
    with open(AUTH_KEYS, "rb") as fp:
        contents = fp.read()
    assert (
        EXPECTED_PUB_CONTENT not in contents
    ), "authorized_keys already contains the pre-seeded public key line; it should not before the task starts"