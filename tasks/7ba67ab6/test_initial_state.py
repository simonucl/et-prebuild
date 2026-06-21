# test_initial_state.py
#
# This pytest suite validates the initial filesystem state that
# MUST exist before the learner executes any commands.
#
# 1. /home/user/cicd must exist as a directory.
# 2. /home/user/cicd/pipeline.ini must exist with the exact, pristine
#    contents specified in the task description (including blank lines
#    and final newline).
# 3. /home/user/cicd/build_info.log must NOT exist yet; the learner is
#    expected to create it.
#
# Any deviation from this initial state will cause the suite to fail
# with a clear, human-readable message.

import pathlib
import textwrap
import pytest


CICD_DIR = pathlib.Path("/home/user/cicd")
PIPELINE_INI = CICD_DIR / "pipeline.ini"
BUILD_INFO_LOG = CICD_DIR / "build_info.log"

# The exact contents the grader expects *before* the learner starts.
EXPECTED_PIPELINE_INI_CONTENT = textwrap.dedent(
    """\
    [metadata]
    project_name = Nebula
    build_number = 42

    [deploy]
    envs = dev,staging,prod
    strategy = rolling

    [notifications]
    slack = true
    email = false
    """
)

def test_cicd_directory_exists():
    assert CICD_DIR.exists(), (
        f"Required directory '{CICD_DIR}' is missing. "
        "The exercise expects the CI/CD files to live here."
    )
    assert CICD_DIR.is_dir(), f"'{CICD_DIR}' exists but is not a directory."


def test_pipeline_ini_exists_with_expected_content():
    assert PIPELINE_INI.exists(), (
        f"Required file '{PIPELINE_INI}' is missing. "
        "It should already be present before the learner starts."
    )
    assert PIPELINE_INI.is_file(), f"'{PIPELINE_INI}' exists but is not a regular file."

    content = PIPELINE_INI.read_text(encoding="utf-8")
    # Ensure a final newline so the exact string comparison is deterministic.
    if not content.endswith("\n"):
        pytest.fail(
            f"'{PIPELINE_INI}' must end with a single trailing newline. "
            "It currently does not."
        )

    assert content == EXPECTED_PIPELINE_INI_CONTENT, (
        f"Contents of '{PIPELINE_INI}' do not match the expected pre-task state.\n"
        "Expected:\n"
        "--------------------\n"
        f"{EXPECTED_PIPELINE_INI_CONTENT}"
        "--------------------\n"
        "Actual:\n"
        "--------------------\n"
        f"{content}"
        "--------------------"
    )


def test_build_info_log_does_not_exist_yet():
    assert not BUILD_INFO_LOG.exists(), (
        f"'{BUILD_INFO_LOG}' already exists, but it should be created "
        "by the learner during the exercise, not beforehand."
    )