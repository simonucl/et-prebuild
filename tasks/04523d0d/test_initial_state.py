# test_initial_state.py
#
# This test-suite verifies that the **initial** filesystem state is
# exactly what the specification guarantees _before_ the student’s
# backup script is executed.  It deliberately does **not** check for
# the absence of additional files (e.g. a pre-existing archive that
# the examiner might place to test the “rename old archive” logic),
# but it _does_ insist that the essential files and directories
# already promised by the task are present and correct.

import os
import pytest

HOME = "/home/user"

FILES_WITH_CONTENT = {
    f"{HOME}/data/projects/readme.txt": "Project README\n",
    f"{HOME}/data/projects/code.py": 'print("Hello World")\n',
    f"{HOME}/data/reports/report1.txt": "Quarterly report Q1\n",
}

DIRECTORIES = [
    f"{HOME}/archives",
    f"{HOME}/backup_logs",
]


@pytest.mark.parametrize("path,expected_content", FILES_WITH_CONTENT.items())
def test_required_files_exist_with_correct_content(path, expected_content):
    """
    Each required data file must exist and contain the exact,
    spec-mandated content (including the trailing newline).
    """
    assert os.path.isfile(
        path
    ), f"Required file missing: {path!r}. It must exist before the backup runs."

    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()

    assert (
        content == expected_content
    ), (
        f"File {path!r} has unexpected content.\n"
        f"Expected (repr): {expected_content!r}\n"
        f"Got      (repr): {content!r}"
    )


@pytest.mark.parametrize("directory", DIRECTORIES)
def test_required_directories_exist(directory):
    """
    The archives and backup_logs directories must already exist
    so that the student’s script can write into them.
    """
    assert os.path.isdir(
        directory
    ), f"Required directory missing: {directory!r}. It must exist before the backup runs."

    # We purposefully do NOT assert emptiness; the examiner may seed
    # the directory with files to test error-recovery behaviour.