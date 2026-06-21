# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the learner attempts the benchmarking exercise.

import os
import stat
import pytest

POLICY_DIR = "/home/user/policy"
POLICY_SCRIPT = "/home/user/policy/check_policy.sh"
BENCHMARK_DIR = "/home/user/benchmark_results"

EXPECTED_POLICY_CONTENT = (
    "#!/bin/bash\n"
    "sleep 0.05\n"
    'echo "Policy PASSED"\n'
)


def test_policy_directory_exists():
    assert os.path.isdir(POLICY_DIR), (
        f"Required directory {POLICY_DIR} is missing or not a directory."
    )

    dir_mode = stat.S_IMODE(os.stat(POLICY_DIR).st_mode)
    assert dir_mode & stat.S_IXUSR, (
        f"Directory {POLICY_DIR} must be searchable/executable by the user "
        f"(got mode {oct(dir_mode)})."
    )


def test_policy_script_exists_and_is_executable():
    assert os.path.isfile(POLICY_SCRIPT), (
        f"Required script {POLICY_SCRIPT} is missing."
    )

    file_mode = stat.S_IMODE(os.stat(POLICY_SCRIPT).st_mode)
    assert file_mode & stat.S_IXUSR, (
        f"Script {POLICY_SCRIPT} is not executable by the user "
        f"(got mode {oct(file_mode)})."
    )


def test_policy_script_contents_are_exact():
    with open(POLICY_SCRIPT, "rb") as fh:
        raw = fh.read()

    # Ensure no CRLF line endings.
    assert b"\r" not in raw, (
        f"Script {POLICY_SCRIPT} must use LF line endings only."
    )

    text = raw.decode("utf-8")
    assert text == EXPECTED_POLICY_CONTENT, (
        f"Script {POLICY_SCRIPT} does not have the expected contents.\n"
        f"Expected:\n{EXPECTED_POLICY_CONTENT!r}\nGot:\n{text!r}"
    )


def test_benchmark_directory_does_not_exist_yet():
    assert not os.path.exists(BENCHMARK_DIR), (
        f"The directory {BENCHMARK_DIR} should NOT exist before the task is run."
    )