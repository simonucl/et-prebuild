# test_initial_state.py
"""
Pytest suite to validate the initial state of the operating system / filesystem
before the student begins the task.

This file checks ONLY for resources that must already exist and deliberately
avoids checking for any artefacts that the student is expected to create.
"""

import os
import pytest


def test_mlops_directory_exists():
    """
    Verify that the base directory /home/user/mlops/ is present.

    The entire exercise assumes that this directory exists prior to any
    further actions; if it is missing the student should create it first.
    """
    mlops_dir = "/home/user/mlops"
    assert os.path.isdir(
        mlops_dir
    ), f"Required directory '{mlops_dir}' does not exist. Please create it before proceeding."