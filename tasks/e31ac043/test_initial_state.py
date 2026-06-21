# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem state
# for the “Integration-developer scenario – detached signature verification and
# subsequent symmetric encryption” exercise.
#
# These checks run *before* the student performs any actions.  They confirm that
# the starting material is present and correct, while intentionally avoiding any
# assertions about the files that the student is expected to create later.
#
# Tested items
# ------------
# 1.  /home/user/work/integration/            … must exist and be a directory.
# 2.  /home/user/work/integration/message.txt … must exist, be UTF-8 text,
#                                               contain exactly three lines
#                                               (including trailing LF) with
#                                               the mandated contents.
# 3.  /home/user/work/integration/message.txt.sig  … must exist and be non-empty.
# 4.  /home/user/work/integration/partner_pub.asc  … must exist and be non-empty.
# 5.  `gpg` must be available in the current PATH.
#
# Nothing in this file checks for the presence or absence of
# verification.log or message.txt.gpg, because those artefacts are
# expected to be produced by the student *after* these tests pass.

import os
import shutil
from pathlib import Path

# Base directory for the exercise
BASE_DIR = Path("/home/user/work/integration").resolve()

# Expected file paths
MESSAGE_TXT     = BASE_DIR / "message.txt"
MESSAGE_SIG     = BASE_DIR / "message.txt.sig"
PARTNER_PUB_ASC = BASE_DIR / "partner_pub.asc"


def test_base_directory_exists():
    """The integration working directory must exist."""
    assert BASE_DIR.is_dir(), (
        f"Required directory not found: {BASE_DIR}. "
        "Verify that the exercise resources were unpacked in the right place."
    )


def test_message_txt_content():
    """
    message.txt must exist, be UTF-8, and contain the exact three required lines
    with a trailing newline.
    """
    assert MESSAGE_TXT.is_file(), f"Missing file: {MESSAGE_TXT}"
    try:
        data = MESSAGE_TXT.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError(
            f"{MESSAGE_TXT} is not valid UTF-8: {exc}"
        ) from exc

    # Must end with a single LF (so that splitlines() counts the final empty
    # string as not present).
    assert data.endswith("\n"), (
        f"{MESSAGE_TXT} must end with a single newline (LF) character."
    )

    lines = data.splitlines()  # keeps no '\n', trailing LF already verified
    assert len(lines) == 3, (
        f"{MESSAGE_TXT} must contain exactly three lines; found {len(lines)}."
    )

    expected = [
        "POST /v1/payments",
        "X-Correlation-ID: 123e4567-e89b-12d3-a456-426614174000",
        '{"amount":42}',
    ]
    for idx, (want, got) in enumerate(zip(expected, lines), start=1):
        assert got == want, (
            f"{MESSAGE_TXT}, line {idx}: expected {want!r}, found {got!r}."
        )


def test_signature_file_exists_and_non_empty():
    """The detached signature file must exist and not be empty."""
    assert MESSAGE_SIG.is_file(), f"Missing detached signature: {MESSAGE_SIG}"
    assert MESSAGE_SIG.stat().st_size > 0, (
        f"Detached signature file {MESSAGE_SIG} is empty."
    )


def test_partner_public_key_exists_and_non_empty():
    """The partner's ASCII-armoured public key must exist and not be empty."""
    assert PARTNER_PUB_ASC.is_file(), f"Missing public key: {PARTNER_PUB_ASC}"
    assert PARTNER_PUB_ASC.stat().st_size > 0, (
        f"Public-key file {PARTNER_PUB_ASC} is empty."
    )


def test_gpg_is_available():
    """The GnuPG executable must be discoverable in PATH."""
    gpg_path = shutil.which("gpg")
    assert gpg_path is not None, (
        "The `gpg` executable is not available in PATH. "
        "Install GnuPG or adjust PATH accordingly."
    )
    # Extra sanity: file exists and is executable
    assert os.access(gpg_path, os.X_OK), (
        f"`gpg` found at {gpg_path} but is not executable."
    )