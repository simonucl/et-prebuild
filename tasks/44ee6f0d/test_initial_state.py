# test_initial_state.py
#
# Pytest suite that validates the machine state *before* the student’s
# release-moving script is executed.

import os
import stat
import tarfile
from pathlib import Path

import pytest

HOME = Path("/home/user")
INCOMING = HOME / "incoming"
EXPECTED_TXT = HOME / "expected_release.txt"
REPOSITORY = HOME / "repository"
RELEASE_LOG = HOME / "release.log"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _assert_is_regular_file(path: Path, msg: str = ""):
    assert path.exists(), f"Missing file: {path}"
    assert path.is_file(), f"Expected a regular file at {path!s} but found something else."
    mode = path.stat().st_mode
    assert stat.S_ISREG(mode), msg or f"{path} is not a regular file"


def _assert_is_directory(path: Path):
    assert path.exists(), f"Missing directory: {path}"
    assert path.is_dir(), f"Expected {path} to be a directory."


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_required_directories_exist():
    """/home/user and /home/user/incoming must already exist."""
    _assert_is_directory(HOME)
    _assert_is_directory(INCOMING)


def test_expected_release_txt_contents():
    """
    /home/user/expected_release.txt must exist and contain exactly the three
    expected lines, in order, with LF line endings and a final newline.
    """
    _assert_is_regular_file(EXPECTED_TXT)

    raw = EXPECTED_TXT.read_bytes()
    assert raw.endswith(b"\n"), (
        "expected_release.txt must end with a single LF newline."
    )

    lines = raw.decode("utf-8").splitlines()
    expected_lines = ["core-1.0", "util-1.2", "gui-3.5"]
    assert (
        lines == expected_lines
    ), f"expected_release.txt contents do not match.\nExpected: {expected_lines}\nFound: {lines}"


@pytest.mark.parametrize(
    "artifact,internal_name,internal_text",
    [
        ("core-1.0", "core.txt", "This is the core artifact\n"),
        ("util-1.2", "util.txt", "This is the util artifact\n"),
    ],
)
def test_incoming_tarballs_present_and_correct(artifact, internal_name, internal_text):
    """
    The two required .tar.gz files must already be present in /incoming and
    contain exactly the expected single file with the correct contents.
    """
    tgz_path = INCOMING / f"{artifact}.tar.gz"
    _assert_is_regular_file(
        tgz_path,
        msg=f"Missing required tarball {tgz_path}. The build script expects it to be present before execution.",
    )

    # Validate tarball structure
    with tarfile.open(tgz_path, "r:gz") as tf:
        members = tf.getmembers()
        names = [m.name for m in members if m.isfile()]
        assert (
            names == [internal_name]
        ), f"{tgz_path} should contain exactly one file named {internal_name}; found {names!r}"

        extracted = tf.extractfile(internal_name)
        assert extracted is not None, f"Could not read {internal_name} inside {tgz_path}"
        contents = extracted.read().decode("utf-8")
        assert (
            contents == internal_text
        ), f"Contents of {internal_name} inside {tgz_path} do not match expected text."


def test_missing_gui_tarball_is_intentional():
    """
    gui-3.5.tar.gz must NOT exist in /incoming by design.
    """
    absent_path = INCOMING / "gui-3.5.tar.gz"
    assert not absent_path.exists(), (
        "gui-3.5.tar.gz is deliberately absent to test error handling; "
        "it should NOT be present before the student runs their script."
    )


def test_no_output_state_yet():
    """
    Output artefacts must *not* exist before the student code runs.
    """
    assert not REPOSITORY.exists(), (
        f"{REPOSITORY} should not exist yet; the student's script must create it."
    )
    assert not RELEASE_LOG.exists(), (
        f"{RELEASE_LOG} should not exist yet; the student's script must create it."
    )