# test_initial_state.py
# Pytest suite that validates the *initial* filesystem state
# before the student begins the task.

import os
import pytest

DEV_UTILS_DIR = "/home/user/dev-utils"
WORDS_FILE = os.path.join(DEV_UTILS_DIR, "words.txt")


def test_dev_utils_directory_exists():
    """
    The helper-utilities directory must already be present.
    """
    assert os.path.isdir(DEV_UTILS_DIR), (
        f"Required directory {DEV_UTILS_DIR!r} is missing. "
        "Create it before starting the task."
    )


def test_words_txt_exists_with_expected_content():
    """
    /home/user/dev-utils/words.txt must exist and contain the
    expected seven-line word list **exactly** as specified in
    the task description.
    """
    assert os.path.isfile(WORDS_FILE), (
        f"Required file {WORDS_FILE!r} is missing. "
        "It must be in place before you start."
    )

    with open(WORDS_FILE, "r", encoding="utf-8") as fh:
        file_contents = fh.read()

    # Ensure the file is not empty.
    assert file_contents, f"{WORDS_FILE!r} is empty; expected a non-empty word list."

    # Compare the actual lines (stripped of the final newline) with the expected list.
    actual_lines = file_contents.strip().splitlines()
    expected_lines = [
        "apple",
        "banana",
        "apple",
        "orange",
        "banana",
        "apple",
        "grape",
    ]
    assert actual_lines == expected_lines, (
        f"Contents of {WORDS_FILE!r} do not match the expected fixture.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Found lines:\n{actual_lines}"
    )