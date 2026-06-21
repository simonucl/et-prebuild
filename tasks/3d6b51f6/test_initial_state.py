# test_initial_state.py
#
# Pytest suite to validate the *initial* filesystem state before the
# student performs any workflow-setup actions.
#
# Validation focus (pre-conditions only):
#   • /home/user/sample_images.txt must exist.
#   • The file must contain the exact two expected lines.
#
# We deliberately do NOT check for the presence or absence of any files or
# directories that the student is expected to create (e.g. /home/user/workflows
# tree, run.sh, setup.log, etc.), in accordance with the grading-suite rules.

import os
from pathlib import Path

SAMPLE_FILE = Path("/home/user/sample_images.txt")
EXPECTED_CONTENT = "raw_image_01.jpg\nraw_image_02.jpg"

def test_sample_images_file_exists():
    """
    The initial environment must provide exactly one file at the known path.
    """
    assert SAMPLE_FILE.is_file(), (
        f"Required file {SAMPLE_FILE} is missing. "
        "The starting environment should include this file with the sample "
        "image list before any workflow setup steps are run."
    )

def test_sample_images_file_content():
    """
    The sample_images.txt file must contain the two expected lines, with no
    trailing newline after the second line.
    """
    content = SAMPLE_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_CONTENT, (
        f"Content of {SAMPLE_FILE} is incorrect.\n"
        f"Expected exactly:\n{EXPECTED_CONTENT!r}\n"
        f"Got:\n{content!r}"
    )