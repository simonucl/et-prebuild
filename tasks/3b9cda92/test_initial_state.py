# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state
# for the “Generate an image-frequency report with sort & uniq” task.
#
# It checks the following pre-conditions _before_ the student’s solution
# is run:
#
# 1. The source file /home/user/images_to_migrate.log exists and is a file.
# 2. The file content is exactly the 11 lines that the grading rubric expects
#    (including the final newline).
#
# No assertions are made about any output artefacts – especially
# /home/user/image_frequency.report – because students have not yet
# performed their actions, and the grading instructions forbid testing
# for output files at this stage.

from pathlib import Path
import pytest

SOURCE_PATH = Path("/home/user/images_to_migrate.log")

EXPECTED_LINES = [
    "nginx:1.19",
    "redis:6",
    "nginx:1.19",
    "mongo:4.4",
    "nginx:1.19",
    "redis:6",
    "postgres:12",
    "mongo:4.4",
    "redis:6",
    "redis:6",
    "postgres:12",
]

# Build the canonical string, including the trailing newline
EXPECTED_CONTENT = "\n".join(EXPECTED_LINES) + "\n"


def test_source_file_exists_and_is_file():
    """Ensure the source log file exists and is a regular file."""
    assert SOURCE_PATH.exists(), (
        f"Required source file {SOURCE_PATH} is missing. "
        "It should already be present before you begin."
    )
    assert SOURCE_PATH.is_file(), (
        f"{SOURCE_PATH} exists but is not a regular file."
    )


def test_source_file_contents_are_correct():
    """Verify the exact contents of the source log file."""
    actual_content = SOURCE_PATH.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_CONTENT, (
        "The content of /home/user/images_to_migrate.log is not as expected.\n"
        "Expected:\n"
        f"{EXPECTED_CONTENT!r}\n"
        "Got:\n"
        f"{actual_content!r}"
    )