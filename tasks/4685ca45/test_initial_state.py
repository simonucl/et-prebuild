# test_initial_state.py
"""
Pytest suite to verify the machine's **initial** state _before_ the student
starts working on the “dotenv + Bash workflow” exercise.

The tests purposefully avoid touching (or even mentioning) any of the
deliverable paths such as
    /home/user/workflows/env-demo
because those will be created _by the student_ and must therefore not be
present in the pristine environment.

Instead, we assert that:
1. The home directory `/home/user` exists and is writable.
2. A POSIX-compatible `bash` binary is available in `$PATH`.
3. None of the workflow-specific environment variables are pre-defined,
   ensuring the student starts from a clean shell state.
"""

import os
import pathlib
import tempfile
import shutil

HOME = pathlib.Path("/home/user")


def test_home_directory_exists_and_writable():
    """`/home/user` must exist and the current user must be able to write there."""
    assert HOME.exists(), f"Expected home directory {HOME} to exist."
    assert HOME.is_dir(), f"{HOME} exists but is not a directory."
    # Try to create and delete a temporary file to confirm write permission
    try:
        tmp_file = HOME / ".pytest_write_test"
        with tmp_file.open("w") as fp:
            fp.write("ok")
    finally:
        if tmp_file.exists():
            tmp_file.unlink()

    assert not tmp_file.exists(), (
        f"Failed to clean up temporary file inside {HOME}. Check write permissions."
    )


def test_bash_binary_is_available():
    """A POSIX‐compatible `bash` must be discoverable via `shutil.which`."""
    bash_path = shutil.which("bash")
    assert (
        bash_path is not None
    ), "No `bash` executable found in PATH; the exercise requires Bash."
    assert pathlib.Path(bash_path).exists(), (
        f"`bash` was reported at {bash_path}, but the file does not exist."
    )


def test_workflow_variables_not_predefined():
    """
    Ensure that the exercise-specific variables are **not** already present
    in the session environment.  Students must define them themselves.
    """
    forbidden_vars = {"APP_NAME", "APP_VERSION", "API_KEY"}
    preexisting = forbidden_vars.intersection(os.environ)
    assert (
        not preexisting
    ), f"The following variables are unexpectedly set in the environment: {', '.join(sorted(preexisting))}"