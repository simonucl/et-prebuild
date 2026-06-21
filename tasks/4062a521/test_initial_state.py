# test_initial_state.py
#
# Pytest suite to verify the MACHINE'S INITIAL STATE *before* the student
# completes the “daily cron task staging” exercise.
#
# The environment is expected to be completely clean: the directory
# /home/user/scheduled_tasks and every file that the student is supposed to
# create must be ABSENT.  These tests guarantee that the student starts from
# a blank slate and that any artifacts which appear later were indeed created
# by the student.

import os
import stat
import pytest

BASE_DIR = "/home/user/scheduled_tasks"
FILES = {
    "clean_tmp.sh",
    "cron_job.txt",
    "task_status.log",
}

@pytest.fixture(scope="module")
def scheduled_tasks_exists():
    """
    Helper fixture that simply returns True/False depending on whether
    the scheduled_tasks directory exists.  Used by multiple tests so that
    pytest does the filesystem lookup only once per module.
    """
    return os.path.exists(BASE_DIR)

def test_scheduled_tasks_directory_absent(scheduled_tasks_exists):
    """
    The directory /home/user/scheduled_tasks should NOT exist yet.
    If it is present at test time, the exercise has not started from a
    clean slate, which could mask errors in the student’s solution.
    """
    assert not scheduled_tasks_exists, (
        f"Pre-exercise directory {BASE_DIR!r} already exists. "
        "The workspace must begin empty so the student’s actions are measurable."
    )

@pytest.mark.parametrize("filename", sorted(FILES))
def test_required_files_absent(filename):
    """
    None of the target files should exist before the student begins the task.
    """
    full_path = os.path.join(BASE_DIR, filename)
    assert not os.path.exists(full_path), (
        f"Pre-exercise file {full_path!r} already exists. "
        "The environment must start without any staged cron artifacts."
    )

def test_no_executable_bits_leaked():
    """
    If, contrary to expectations, /home/user/scheduled_tasks/clean_tmp.sh is
    present *and* executable before the student starts, fail with an explicit
    message pointing out the premature presence of the script.
    """
    script_path = os.path.join(BASE_DIR, "clean_tmp.sh")
    if os.path.exists(script_path):
        mode = os.stat(script_path).st_mode
        is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        assert not is_executable, (
            f"Found pre-existing executable {script_path!r}. "
            "The student must be the one to create and mark it executable."
        )