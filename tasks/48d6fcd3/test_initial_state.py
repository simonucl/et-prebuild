# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state expected by the assignment “DevOps debug minimal Python-package setup”.
#
# Only the Python standard library and pytest are used.
# Every assertion contains a clear error message so that any deviation from
# the specification is obvious to the student.

import os
import subprocess
from pathlib import Path

BASE_DIR = Path("/home/user/devops_debug")
VENV_DIR = BASE_DIR / "venv"
LOG_DIR = BASE_DIR / "logs"

ACTIVE_PACKAGES_LOG = LOG_DIR / "active_packages.log"
SETUP_COMPLETE_FLAG = LOG_DIR / "setup_complete.flag"

EXPECTED_ACTIVE_PACKAGES_CONTENT = (
    b"requests==2.28.1\n"
    b"boto3==1.34.59\n"
)

EXPECTED_PACKAGES = {
    "requests": "2.28.1",
    "boto3": "1.34.59",
}


def test_base_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Directory {BASE_DIR} does not exist. "
        "The setup must create /home/user/devops_debug/."
    )


def test_venv_directory_and_activate_file():
    assert VENV_DIR.is_dir(), (
        f"Virtual-environment directory {VENV_DIR} is missing."
    )
    activate_script = VENV_DIR / "bin" / "activate"
    assert activate_script.is_file(), (
        f"{activate_script} is missing. Has the venv been created correctly?"
    )


def test_logs_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Logs directory {LOG_DIR} is missing."
    )


def test_setup_complete_flag_is_empty():
    assert SETUP_COMPLETE_FLAG.is_file(), (
        f"Required empty file {SETUP_COMPLETE_FLAG} is missing."
    )
    size = SETUP_COMPLETE_FLAG.stat().st_size
    assert size == 0, (
        f"{SETUP_COMPLETE_FLAG} must be completely empty (size 0 bytes); "
        f"found size {size}."
    )


def test_active_packages_log_contents_and_line_endings():
    assert ACTIVE_PACKAGES_LOG.is_file(), (
        f"Log file {ACTIVE_PACKAGES_LOG} is missing."
    )
    content = ACTIVE_PACKAGES_LOG.read_bytes()
    # 1) Exact byte-for-byte match (guarantees correct order & trailing newline)
    assert content == EXPECTED_ACTIVE_PACKAGES_CONTENT, (
        f"{ACTIVE_PACKAGES_LOG} contents are incorrect.\n"
        f"Expected (bytes): {EXPECTED_ACTIVE_PACKAGES_CONTENT!r}\n"
        f"Found   (bytes): {content!r}"
    )
    # 2) Ensure no Windows CRLFs present
    assert b"\r" not in content, (
        f"{ACTIVE_PACKAGES_LOG} must use Unix LF line endings, "
        "but CR characters were detected."
    )


def _run_in_venv(*args) -> str:
    """
    Execute a command *inside* the virtual environment and return stdout (str).

    We call the venv's Python executable so that pip and package
    discovery run in that environment only.
    """
    python_exe = VENV_DIR / "bin" / "python"
    assert python_exe.is_file(), (
        f"{python_exe} is missing; the virtual environment appears corrupt."
    )
    cmd = [str(python_exe), "-m"] + list(args)
    try:
        output = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as exc:
        raise AssertionError(
            f"Command {' '.join(cmd)!r} failed with exit code {exc.returncode} "
            f"and output:\n{exc.output}"
        ) from None
    return output


def test_required_packages_installed_with_correct_versions():
    """
    For each required package, verify that:
    • It is installed inside the venv, and
    • The pinned version matches exactly.
    """
    for package, expected_version in EXPECTED_PACKAGES.items():
        out = _run_in_venv("pip", "show", package)
        lines = [line.strip() for line in out.splitlines() if line.strip()]
        version_lines = [ln for ln in lines if ln.lower().startswith("version:")]
        assert version_lines, (
            f"'pip show {package}' inside the venv returned no version info. "
            f"Package may not be installed."
        )
        found_version = version_lines[0].split(":", 1)[1].strip()
        assert found_version == expected_version, (
            f"Package {package} is installed with version {found_version}, "
            f"but version {expected_version} is required."
        )