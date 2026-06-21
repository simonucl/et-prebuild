# test_initial_state.py
#
# This pytest suite verifies that the container starts in the state
# expected by the assignment *before* the student runs any commands.
#
# It intentionally avoids checking for any artefacts the student is
# supposed to create later (e.g. latest_sync.log).  Only the initial
# filesystem layout is validated.

import os
import textwrap

HOME = "/home/user"

SRC_DIR = os.path.join(HOME, "project_data")
DST_DIR = os.path.join(HOME, "remote_backup")
LOG_DIR = os.path.join(HOME, "sync_logs")

SRC_FILES = {
    "data1.txt": textwrap.dedent(
        """\
        Alpha
        Beta
        Gamma
        """
    ),
    "data2.cfg": textwrap.dedent(
        """\
        [settings]
        mode=production
        """
    ),
    "data3.json": textwrap.dedent(
        """\
        {
          "version": 1.2,
          "enabled": true
        }
        """
    ),
}

def _read_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()

def test_source_directory_exists_and_is_directory():
    assert os.path.isdir(SRC_DIR), (
        f"Expected source directory {SRC_DIR!r} to exist and be a directory."
    )

def test_source_directory_contains_expected_files():
    actual_files = set(os.listdir(SRC_DIR))
    missing = set(SRC_FILES) - actual_files
    extras = actual_files - set(SRC_FILES)
    assert not missing, (
        f"The source directory {SRC_DIR!r} is missing files: {', '.join(sorted(missing))}"
    )
    assert not extras, (
        f"The source directory {SRC_DIR!r} contains unexpected files: "
        f"{', '.join(sorted(extras))}"
    )

def test_source_files_have_correct_contents():
    for filename, expected_content in SRC_FILES.items():
        path = os.path.join(SRC_DIR, filename)
        assert os.path.isfile(path), f"Missing expected file {path!r}"
        content = _read_file(path)
        # Ensure trailing newline in the expected content for reliable comparison
        if not expected_content.endswith("\n"):
            expected_content += "\n"
        assert content == expected_content, (
            f"Contents of {path!r} do not match the expected initial data."
        )

def test_remote_backup_initial_state():
    assert os.path.isdir(DST_DIR), (
        f"Expected destination directory {DST_DIR!r} to exist and be a directory."
    )
    dst_files = os.listdir(DST_DIR)
    assert dst_files == ["data1.txt"], (
        f"Destination directory {DST_DIR!r} should initially contain only "
        f"'data1.txt', but contains: {', '.join(sorted(dst_files)) or 'NO FILES'}"
    )
    stale_path = os.path.join(DST_DIR, "data1.txt")
    assert os.path.isfile(stale_path), f"File {stale_path!r} is missing."
    stale_content = _read_file(stale_path).rstrip("\n")
    assert stale_content == "OldData", (
        f"Initial content of {stale_path!r} should be 'OldData' "
        f"(indicating staleness) but was: {stale_content!r}"
    )

def test_sync_logs_directory_exists_and_is_empty():
    assert os.path.isdir(LOG_DIR), (
        f"Log directory {LOG_DIR!r} must exist before the sync begins."
    )
    contents = os.listdir(LOG_DIR)
    assert contents == [], (
        f"Log directory {LOG_DIR!r} should be empty at the start, "
        f"but contains: {', '.join(sorted(contents))}"
    )