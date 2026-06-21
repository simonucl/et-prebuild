# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating
# system before the student begins working on the “compliance_audit”
# project.  We explicitly **do not** look for any of the files or
# directories that the student is expected to create.  Instead we
# verify that the environment provides the basic tooling and writable
# locations required to complete the task.

import os
import shutil
import subprocess
import tempfile
import textwrap

import pytest


HOME_DIR = "/home/user"


def test_home_directory_exists():
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected home directory {HOME_DIR!r} to exist."


def test_home_directory_writable():
    assert os.access(
        HOME_DIR, os.W_OK | os.X_OK
    ), f"Home directory {HOME_DIR!r} must be writable and traversable by the student process."


def test_make_is_available_and_gnu():
    """
    The project depends on GNU Make for parallel execution.
    """
    make_path = shutil.which("make")
    assert make_path is not None, "'make' command must be available in the PATH."
    assert os.access(
        make_path, os.X_OK
    ), f"'make' was found at {make_path!r} but is not executable."

    try:
        out = subprocess.check_output(
            [make_path, "--version"], text=True, timeout=5
        )
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Invoking 'make --version' failed: {exc}")

    assert (
        "GNU Make" in out
    ), "The available 'make' implementation must be GNU Make."


def test_make_supports_parallel_flag():
    """
    Verify that the installed `make` supports the -j (parallel jobs) flag.
    We compile a trivial Makefile and run it with `-j2`.
    """
    make_path = shutil.which("make")
    assert make_path, "'make' command could not be located in PATH."

    with tempfile.TemporaryDirectory() as tmpdir:
        makefile_path = os.path.join(tmpdir, "Makefile")
        makefile_content = textwrap.dedent(
            """
            .PHONY: all
            all:
            \t@echo parallel-test
            """
        ).lstrip()

        with open(makefile_path, "w", encoding="utf-8") as fp:
            fp.write(makefile_content)

        try:
            out = subprocess.check_output(
                [make_path, "-j2", "-f", makefile_path],
                cwd=tmpdir,
                text=True,
                timeout=10,
            )
        except subprocess.CalledProcessError as exc:  # pragma: no cover
            pytest.fail(
                f"'make -j2' failed on a trivial Makefile "
                f"(return code {exc.returncode}). output:\n{exc.output}"
            )
        except Exception as exc:  # pragma: no cover
            pytest.fail(f"Running 'make -j2' raised an unexpected exception: {exc}")

        assert (
            "parallel-test" in out.strip()
        ), "Running 'make -j2' did not emit the expected output; parallel jobs may not be supported."


def test_posix_sh_exists_and_executable():
    """
    The student will write POSIX-sh scripts; /bin/sh must be present and executable.
    """
    assert os.path.isfile("/bin/sh"), "Missing required interpreter: /bin/sh."
    assert os.access("/bin/sh", os.X_OK), "/bin/sh exists but is not executable."


def test_ls_command_available():
    """
    The final verification requires the `ls` utility.
    """
    ls_path = shutil.which("ls")
    assert ls_path is not None, "'ls' command must be available in the PATH."
    assert os.access(ls_path, os.X_OK), f"Found 'ls' at {ls_path!r} but it is not executable."