# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem/OS state for the
“hardener” version-bump exercise *before* the student begins any work.

The tests purposefully fail fast and supply clear, actionable error
messages whenever the environment does **not** match the canonical
starting snapshot described in the task.
"""

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
HARDENER_DIR = HOME / "hardener"
VERSION_FILE = HARDENER_DIR / "version.txt"
CHANGELOG_FILE = HARDENER_DIR / "CHANGELOG.md"
SSH_CONF = HARDENER_DIR / "harden-ssh.conf"
SYSCTL_CONF = HARDENER_DIR / "harden-sysctl.conf"
BUMP_LOG = HARDENER_DIR / "bump.log"

# ---------------------------------------------------------------------------
# Helper fixtures / functions
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def changelog_lines():
    """
    Return the lines (without trailing newline characters) of CHANGELOG.md.
    The fixture will fail with a descriptive error if the file cannot
    be read for any reason.
    """
    try:
        text = CHANGELOG_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Expected file {CHANGELOG_FILE} to exist but it is missing.")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {CHANGELOG_FILE}: {exc}")

    return text.splitlines()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_hardener_directory_exists_and_is_directory():
    assert HARDENER_DIR.exists(), f"Directory {HARDENER_DIR} is missing."
    assert HARDENER_DIR.is_dir(), f"{HARDENER_DIR} exists but is not a directory."


def test_version_file_content_and_format():
    assert VERSION_FILE.exists(), f"Version file {VERSION_FILE} is missing."

    # Read in *binary* mode so we can examine raw bytes (no automatic newline handling)
    data = VERSION_FILE.read_bytes()

    # The expected semantic version string for the initial state
    expected = b"1.4.2"
    assert (
        data == expected
    ), (
        f"{VERSION_FILE} should contain exactly {expected.decode()} (no newline) "
        f"but instead contains {data.decode(errors='ignore')!r}"
    )

    # Double-check newline absence explicitly for clarity.
    assert b"\n" not in data, (
        f"{VERSION_FILE} must not include a trailing newline "
        f"but one was found."
    )


def test_changelog_starts_with_expected_block(changelog_lines):
    """
    The entire initial CHANGELOG must match the canonical block given in
    the spec.  Using splitlines() makes the check agnostic to a trailing
    newline on the last line while still being strict about line content.
    """
    expected_lines = [
        "## [1.4.2] - 2023-08-07",
        "### Added",
        "- Initial iptables hardening rules.",
        "",
        "### Changed",
        "- Tuned /proc sysctl defaults.",
        "",
        "### Fixed",
        "- Corrected typo in sshd_config example.",
    ]

    assert changelog_lines == expected_lines, (
        "CHANGELOG.md does not match the expected initial content.\n\n"
        "Expected:\n"
        + "\n".join(expected_lines)
        + "\n\nActual:\n"
        + "\n".join(changelog_lines)
    )


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (SSH_CONF, "SSH hardening configuration"),
        (SYSCTL_CONF, "sysctl hardening configuration"),
    ],
)
def test_required_configuration_files_exist(path_obj, description):
    assert path_obj.exists(), f"{description} file {path_obj} is missing."
    assert path_obj.is_file(), f"{path_obj} exists but is not a regular file."


def test_bump_log_does_not_exist_yet():
    """
    `bump.log` must *not* exist in the pristine starting state.
    Its presence would imply the bump has already been attempted.
    """
    assert not BUMP_LOG.exists(), f"Found unexpected file {BUMP_LOG}; the workspace is not clean."