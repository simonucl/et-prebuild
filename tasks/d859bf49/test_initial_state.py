# test_initial_state.py
#
# This test-suite validates the **initial** state of the file-system
# before the student runs any commands for the “backup & log” task.
#
# It deliberately avoids touching or mentioning any of the *output*
# artefacts that the student is supposed to generate later
# (/home/user/remote_host/backups/…  or /home/user/backup_logs/…).
#
# Only stdlib + pytest are used.

import io
from pathlib import Path

import pytest

HOME = Path("/home/user")

DATA_ROOT   = HOME / "data_to_backup"
REMOTE_ROOT = HOME / "remote_host"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    """
    Read *text* from a file, using UTF-8 and preserving newlines exactly
    as they appear in the file.
    """
    with path.open("r", encoding="utf-8", newline="") as f:
        return f.read()


# ---------------------------------------------------------------------------
# 1. Basic directory existence
# ---------------------------------------------------------------------------

def test_required_directories_exist():
    assert DATA_ROOT.is_dir(), (
        f"Required directory missing: {DATA_ROOT}"
    )
    assert REMOTE_ROOT.is_dir(), (
        f"Required directory missing: {REMOTE_ROOT}"
    )


# ---------------------------------------------------------------------------
# 2. `data_to_backup` tree structure and files
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "relative_path",
    [
        "docs/report.txt",
        "images/photo1.jpg",
        "images/photo2.jpg",
        "scripts/cleanup.sh",
    ],
)
def test_source_files_exist(relative_path):
    abs_path = DATA_ROOT / relative_path
    assert abs_path.is_file(), (
        f"Expected source file is missing: {abs_path}"
    )


# ---------------------------------------------------------------------------
# 3. Contents of the source files
# ---------------------------------------------------------------------------

def test_report_txt_content():
    path = DATA_ROOT / "docs" / "report.txt"
    content = read_file(path)

    # It must contain the single word "Quarterly" followed by *exactly*
    # one LF.  We do not rely on the byte count stated in the task text,
    # as that has occasionally been inaccurate.
    assert content.startswith("Quarterly"), (
        f"{path} must start with the word 'Quarterly'"
    )
    assert content.endswith("\n"), (
        f"{path} must end with a single Unix newline (LF)"
    )
    # There must be no extra data after the newline.
    stripped = content.rstrip("\n")
    assert stripped == "Quarterly", (
        f"{path} must contain only the word 'Quarterly' followed by a newline; "
        f"found additional data."
    )


@pytest.mark.parametrize(
    "file_name, expected_prefix",
    [
        ("photo1.jpg", "JPEG_DUMMY_DATA_1"),
        ("photo2.jpg", "JPEG_DUMMY_DATA_2"),
    ],
)
def test_image_dummy_contents(file_name, expected_prefix):
    path = DATA_ROOT / "images" / file_name
    # Read as binary because we do not care about encoding here
    data = path.read_bytes()

    # The dummy data must start with the expected ASCII marker and end with LF
    prefix_bytes = expected_prefix.encode("ascii")
    assert data.startswith(prefix_bytes), (
        f"{path} does not start with expected dummy data "
        f"({expected_prefix!r})."
    )
    assert data.endswith(b"\n"), (
        f"{path} must end with a Unix newline (LF)."
    )


def test_cleanup_script_content():
    path = DATA_ROOT / "scripts" / "cleanup.sh"
    text = read_file(path)

    expected_first_line = "#!/bin/bash"
    expected_second_line = "echo cleanup"

    lines = text.splitlines()
    assert lines[0] == expected_first_line, (
        f"{path} first line must be the shebang '{expected_first_line}'."
    )
    assert len(lines) >= 2 and lines[1] == expected_second_line, (
        f"{path} second line must be '{expected_second_line}'."
    )
    assert text.endswith("\n"), (
        f"{path} must end with a Unix newline (LF)."
    )


# ---------------------------------------------------------------------------
# 4. The “remote host” directory must be empty at the beginning
# ---------------------------------------------------------------------------

def test_remote_host_is_initially_empty():
    contents = list(REMOTE_ROOT.rglob("*"))
    assert not contents, (
        f"{REMOTE_ROOT} should be empty before the task starts, "
        f"but it already contains: {contents}"
    )