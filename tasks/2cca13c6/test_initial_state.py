# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state that must be
# present before the student performs any actions for the compression task.
#
# It checks ONLY for the directories and files that are pre-existing.  It
# purposefully does *not* mention or assert anything about the output artefacts
# that the student will create later (e.g. /home/user/project_backup.tar.gz,
# /home/user/project_backup, /home/user/compression_log.txt).

from pathlib import Path

# ---------- Constants describing the expected initial state -------------

# Directories that must already exist
EXPECTED_DIRS = [
    Path("/home/user"),
    Path("/home/user/project"),
    Path("/home/user/project/utils"),
]

# Files that must already exist together with their exact byte content
EXPECTED_FILES = {
    Path("/home/user/project/main.py"): b'print("Hello from main")\n',
    Path("/home/user/project/README.md"): (
        b"# Project Sample\n"
        b"A tiny project used for compression-task testing.\n"
    ),
    Path("/home/user/project/utils/helper.py"): (
        b"def helper():\n"
        b'    return "helping"\n'
    ),
}

# ------------------------------ Tests ------------------------------------

def test_expected_directories_exist():
    """
    All required directories must exist before the student runs their commands.
    """
    for directory in EXPECTED_DIRS:
        assert directory.is_dir(), (
            f"Required directory missing: {directory}. "
            "Make sure the initial project tree is in place."
        )


def test_expected_files_exist_with_correct_content():
    """
    Each required file must exist and its content must match the specification
    exactly (byte-for-byte).
    """
    for filepath, expected_content in EXPECTED_FILES.items():
        assert filepath.is_file(), (
            f"Required file missing: {filepath}. "
            "The initial project files must be present before starting."
        )

        actual_content = filepath.read_bytes()
        assert actual_content == expected_content, (
            f"File content mismatch in {filepath}.\n"
            "Expected:\n"
            f"{expected_content.decode()!r}\n\n"
            "Found:\n"
            f"{actual_content.decode()!r}"
        )