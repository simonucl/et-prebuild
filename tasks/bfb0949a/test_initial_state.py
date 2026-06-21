# test_initial_state.py
#
# Pytest suite validating the VM *before* the student begins the task.
# It checks that the pre-existing directory /home/user/hardening and its
# configuration files are present and contain the expected, exact contents.
# No assertions are made about any output artefacts that the student
# should create later (archives, restore directories, log files, …).

import os
from pathlib import Path

HARDENING_DIR = Path("/home/user/hardening")
SSHD_CONFIG = HARDENING_DIR / "sshd_config"
SYSCTL_CONF = HARDENING_DIR / "sysctl.conf"

EXPECTED_CONTENTS = {
    SSHD_CONFIG: "PasswordAuthentication no\nPermitRootLogin no\n",
    SYSCTL_CONF: (
        "net.ipv4.ip_forward = 0\n"
        "kernel.randomize_va_space = 2\n"
    ),
}


def test_hardening_directory_exists():
    """Ensure /home/user/hardening exists and is a directory."""
    assert HARDENING_DIR.exists(), (
        f"Expected directory {HARDENING_DIR} is missing."
    )
    assert HARDENING_DIR.is_dir(), (
        f"{HARDENING_DIR} exists but is not a directory."
    )


def test_expected_files_present_and_only_them():
    """
    The hardening directory must contain exactly the two expected files
    (no more, no less) and both must be regular files.
    """
    entries = sorted(p.name for p in HARDENING_DIR.iterdir())
    expected_entries = sorted(p.name for p in EXPECTED_CONTENTS)
    assert entries == expected_entries, (
        f"{HARDENING_DIR} should contain exactly {expected_entries}, "
        f"but found {entries}."
    )

    for file_path in EXPECTED_CONTENTS:
        assert file_path.is_file(), f"{file_path} is missing or not a file."


def test_file_contents_exact_match():
    """
    Each file must contain the exact expected text including newlines.
    """
    for file_path, expected_text in EXPECTED_CONTENTS.items():
        try:
            actual_text = file_path.read_text(encoding="utf-8")
        except Exception as exc:
            raise AssertionError(f"Could not read {file_path}: {exc}") from exc

        assert actual_text == expected_text, (
            f"Contents of {file_path} are not as expected.\n"
            f"Expected:\n{repr(expected_text)}\n\n"
            f"Actual:\n{repr(actual_text)}"
        )