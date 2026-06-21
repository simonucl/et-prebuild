# test_initial_state.py
#
# This pytest suite validates the initial state of the operating system
# *before* the student starts working on the task.  According to the task
# description, only the optimisation template must already exist; no other
# artefacts (the ones the student is supposed to create) must be checked at
# this stage.
#
# Rules recap:
#   • Only stdlib + pytest are used.
#   • We test for the *presence* of the template directory and file and
#     validate the exact file content.
#   • We explicitly do NOT test for the presence or absence of any output
#     directories / files the student will create later on.

import os
from pathlib import Path

TEMPLATE_DIR = Path("/home/user/templates/optimization")
TEMPLATE_FILE = TEMPLATE_DIR / "solver_template.conf"

EXPECTED_TEMPLATE_CONTENT = (
    "# Solver Configuration Template\n"
    "algorithm=template\n"
    "learning_rate=0.01\n"
    "max_iterations=200\n"
    "tolerance=1e-6\n"
)


def test_template_directory_exists():
    assert TEMPLATE_DIR.exists(), (
        f"Required directory not found: {TEMPLATE_DIR}. "
        "The template directory must be present before the student starts."
    )
    assert TEMPLATE_DIR.is_dir(), (
        f"Expected {TEMPLATE_DIR} to be a directory, but it exists as a different "
        "file type. Ensure a directory is provided."
    )


def test_template_file_exists_and_content_is_correct():
    assert TEMPLATE_FILE.exists(), (
        f"Required template file not found: {TEMPLATE_FILE}. "
        "The template must exist before the student starts."
    )
    assert TEMPLATE_FILE.is_file(), (
        f"Expected {TEMPLATE_FILE} to be a regular file, but it is not."
    )

    actual_content = TEMPLATE_FILE.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_TEMPLATE_CONTENT, (
        "Template file content does not match the expected initial state.\n\n"
        "Expected:\n"
        "----------------\n"
        f"{EXPECTED_TEMPLATE_CONTENT}"
        "----------------\n\n"
        "Actual:\n"
        "----------------\n"
        f"{actual_content}"
        "----------------\n"
        "The template must remain unmodified at the start."
    )