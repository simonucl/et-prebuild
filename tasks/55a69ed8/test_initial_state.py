# test_initial_state.py
#
# This pytest suite validates the **initial** state of the file-system
# before the learner writes any solution code.  It asserts that:
#
# 1. The legacy helper script `/home/user/tools/fake_benchmark.sh`
#    a) exists,
#    b) is a regular file,
#    c) is executable by the owner, and
#    d) contains the exact four expected lines.
#
# 2. The target output file `/home/user/benchmark/compile_speed.log`
#    does *not* yet exist (it will be produced by the learner later).
#
# Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest


SCRIPT_PATH = Path("/home/user/tools/fake_benchmark.sh")
EXPECTED_SCRIPT_LINES = [
    '#!/usr/bin/env bash',
    'echo -e "\\treal: 0.12"',
    'echo -e "\\tuser: 0.03"',
    'echo -e "\\tsys: 0.01"',
]

OUTPUT_FILE = Path("/home/user/benchmark/compile_speed.log")


def test_fake_benchmark_script_present_and_correct():
    """
    Validate that the legacy helper script is present, executable, and
    has exactly the expected contents.
    """
    # 1a / 1b — existence and type
    assert SCRIPT_PATH.exists(), (
        f"Required script not found: {SCRIPT_PATH}"
    )
    assert SCRIPT_PATH.is_file(), (
        f"Expected {SCRIPT_PATH} to be a regular file."
    )

    # 1c — executable by owner
    st_mode = SCRIPT_PATH.stat().st_mode
    assert st_mode & stat.S_IXUSR, (
        f"{SCRIPT_PATH} must be executable by its owner (missing +x)."
    )

    # 1d — exact content
    with SCRIPT_PATH.open("r", encoding="utf-8") as fh:
        file_lines = fh.read().splitlines()  # strips newline characters

    assert file_lines == EXPECTED_SCRIPT_LINES, (
        "Content of {0} does not match expectation.\n"
        "Expected lines:\n{1}\n\nActual lines:\n{2}".format(
            SCRIPT_PATH,
            "\n".join(EXPECTED_SCRIPT_LINES),
            "\n".join(file_lines),
        )
    )


def test_output_file_not_yet_created():
    """
    Confirm that the learner has not (yet) created the target log file.
    The exercise instructions require the file to be *created* by the
    learner's solution, so it must be absent at the initial state.
    """
    assert not OUTPUT_FILE.exists(), (
        f"{OUTPUT_FILE} already exists, but it should be created by the "
        "learner's solution code, not be present in the starting state."
    )