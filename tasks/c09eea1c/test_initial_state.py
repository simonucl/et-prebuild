# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem
state before the student performs any action for the “log_review_env”
exercise.

The exercise eventually expects the student to create a Python virtual
environment under /home/user/log_review_env and populate it with several
files.  These tests assert that **none** of those artifacts are present
yet.  If any of them already exist, the environment is not clean and the
student would get misleading feedback.

Only the Python standard library and pytest are used, and every failure
message explains exactly what should *not* be there at this stage.
"""

import os
import pathlib
import re

# ---------------------------------------------------------------------------#
# Constants                                                                   #
# ---------------------------------------------------------------------------#
HOME_DIR = pathlib.Path("/home/user").expanduser().resolve()
ENV_DIR = HOME_DIR / "log_review_env"
EXPECTED_RELATIVE_ITEMS = {
    pathlib.Path("bin") / "activate",
    pathlib.Path("lib"),
    pathlib.Path("pyvenv.cfg"),
    pathlib.Path("setup.log"),
}


# ---------------------------------------------------------------------------#
# Helper functions                                                            #
# ---------------------------------------------------------------------------#
def _iter_existing_items_under_env():
    """
    Yield pathlib.Path objects for *any* files or directories that already
    exist under /home/user/log_review_env.  The paths are returned *relative*
    to ENV_DIR for clearer error reporting.
    """
    if not ENV_DIR.exists():
        return  # Nothing to iterate

    for root, dirs, files in os.walk(ENV_DIR):
        root_path = pathlib.Path(root)
        for name in dirs + files:
            absolute = root_path / name
            yield absolute.relative_to(ENV_DIR)


# ---------------------------------------------------------------------------#
# Tests                                                                       #
# ---------------------------------------------------------------------------#
def test_log_review_env_does_not_exist():
    """
    The directory /home/user/log_review_env must *not* exist yet.
    If it exists the subsequent grading will be unable to distinguish
    the student's work from pre-existing files.
    """
    assert not ENV_DIR.exists(), (
        f"The directory {ENV_DIR} already exists, but the exercise "
        "requires starting from a clean slate."
    )


def test_no_expected_artifacts_present():
    """
    Even if a rogue /home/user/log_review_env directory does exist, none of
    the files that the final grader will look for should already be present.
    """
    missing = []
    present = []

    for relative_path in EXPECTED_RELATIVE_ITEMS:
        absolute_path = ENV_DIR / relative_path
        if absolute_path.exists():
            present.append(str(relative_path))
        else:
            missing.append(str(relative_path))  # kept for completeness

    assert not present, (
        "The following artifacts already exist but should *not* be present "
        "before the student runs their single shell command:\n"
        + "\n".join(f"  • {p}" for p in sorted(present))
    )


def test_no_leftover_files_in_env_directory():
    """
    If /home/user/log_review_env exists for some reason, ensure it is *completely*
    empty.  The presence of any file or directory indicates the environment
    is not pristine.
    """
    unexpected_items = sorted(map(str, _iter_existing_items_under_env()))
    assert not unexpected_items, (
        f"Found unexpected files/directories inside {ENV_DIR}:\n"
        + "\n".join(f"  • {item}" for item in unexpected_items)
        + "\nPlease ensure the system starts in a clean state."
    )


def test_python_and_venv_modules_available():
    """
    Sanity-check that the host Python installation can create virtual
    environments.  This is *not* part of the student's task, but verifying
    it here helps catch misconfigured execution environments early.
    """
    try:
        import venv  # noqa: F401
    except ImportError:
        pytest.fail(
            "The standard library module 'venv' is missing. "
            "A working Python distribution with venv support is required "
            "for the upcoming exercise."
        )