# test_initial_state.py
#
# Pytest suite that validates the expected *initial* state of the host
# BEFORE the student carries out any actions for the “AcmeCorp Binary
# Repositories” diagnostics task.
#
# These tests confirm only the resources that are guaranteed to exist
# up-front (the truth value), and they ensure that no artefacts that the
# student is supposed to create exist yet.
#
# Rules respected:
# • stdlib + pytest only
# • absolute paths are used
# • no output artefacts are referenced
# • clear failure messages are provided

import os
import re
import stat
from pathlib import Path

import pytest


OPT_BINARIES = Path("/opt/binaries")
ARCHIVES_DIR = OPT_BINARIES / "archives"
HOME_DIAGNOSTICS = Path("/home/user/diagnostics")
LOG_FILE_PATTERN = re.compile(r"^repo_diagnostics_\d{8}_\d{6}\.log$")

# Expected seed files and their *minimum* sizes in bytes
EXPECTED_FILES = {
    OPT_BINARIES / "widget-1.0.0.tar.gz": 35 * 1024 * 1024,   # ≈40 MiB
    OPT_BINARIES / "gadget-2.5.1.zip":    20 * 1024 * 1024,   # ≈25 MiB
    OPT_BINARIES / "libfoo.so":           10 * 1024 * 1024,   # ≈12 MiB
    ARCHIVES_DIR / "legacy.bin":          55 * 1024 * 1024,   # ≈60 MiB
}


def _is_world_readable(path: Path) -> bool:
    """Return True if 'others' have read permission on the given path."""
    mode = path.stat().st_mode
    return bool(mode & stat.S_IROTH)


def test_opt_binaries_structure_exists_and_is_readable():
    assert OPT_BINARIES.is_dir(), (
        f"Required directory {OPT_BINARIES} is missing. "
        "It must exist before the student begins."
    )
    assert _is_world_readable(OPT_BINARIES), (
        f"Directory {OPT_BINARIES} must be world-readable (others +r)."
    )

    assert ARCHIVES_DIR.is_dir(), (
        f"Required sub-directory {ARCHIVES_DIR} is missing."
    )
    assert _is_world_readable(ARCHIVES_DIR), (
        f"Directory {ARCHIVES_DIR} must be world-readable (others +r)."
    )


@pytest.mark.parametrize("filepath,min_size", EXPECTED_FILES.items())
def test_expected_seed_files_exist_and_have_reasonable_size(filepath: Path, min_size: int):
    assert filepath.is_file(), f"Seed file {filepath} is missing."
    real_size = filepath.stat().st_size
    assert real_size >= min_size, (
        f"Seed file {filepath} looks too small: "
        f"expected at least {min_size} bytes, found {real_size} bytes."
    )
    assert os.access(filepath, os.R_OK), f"Seed file {filepath} is not readable."


def test_diagnostics_directory_empty_or_absent_before_student_action():
    """
    The /home/user/diagnostics directory may or may not exist yet, but in either
    case there must not be any repo_diagnostics_*.log file present *before* the
    student runs their commands.
    """
    if not HOME_DIAGNOSTICS.exists():
        # Directory absent – that is acceptable.
        return

    assert HOME_DIAGNOSTICS.is_dir(), (
        f"{HOME_DIAGNOSTICS} exists but is not a directory."
    )

    # Gather any pre-existing snapshot files
    preexisting_logs = [
        p for p in HOME_DIAGNOSTICS.iterdir()
        if p.is_file() and LOG_FILE_PATTERN.fullmatch(p.name)
    ]

    assert not preexisting_logs, (
        "Diagnostic log files already exist in "
        f"{HOME_DIAGNOSTICS}: {', '.join(p.name for p in preexisting_logs)}\n"
        "The directory must be empty (or absent) before the student starts."
    )