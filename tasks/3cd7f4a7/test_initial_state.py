# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state before the
# student’s shell-based solution is executed.

import os
import stat
import pytest

HOME = "/home/user"
CONFIG_DIR = os.path.join(HOME, "configs")
OUTPUT_DIR = os.path.join(HOME, "output")
CLEAN_DIR = os.path.join(HOME, "clean_configs")

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def read_file(path):
    """Return file contents as bytes; fail loudly if the file is unreadable."""
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except FileNotFoundError:
        pytest.fail(f"Required file {path!s} is missing.")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path!s}: {exc}")


# --------------------------------------------------------------------------- #
# Expected truths                                                             #
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    os.path.join(CONFIG_DIR, "config_20230115.conf"): (
        b"# Sample app config\n"
        b"  host = localhost\n"
        b"port=8080\n"
        b"max_connections = 100\n"
        b"# End\n"
    ),
    os.path.join(CONFIG_DIR, "config_20230410.conf"): (
        b"# Updated config\n"
        b"host = prod.example.com\n"
        b"port = 80\n"
        b"max_connections= 250\n"
        b"timeout = 30\n"
    ),
    os.path.join(CONFIG_DIR, "config_20230718.conf"): (
        b"## Production patch\n"
        b"host=prod.example.com\n"
        b"port=443\n"
        b"max_connections =300\n"
        b"timeout=45\n"
        b"enable_tls = true\n"
        b"#some comment\n"
        b"  cache_size= 512\n"
    ),
}


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_configs_directory_exists_and_is_dir():
    assert os.path.isdir(
        CONFIG_DIR
    ), f"Directory {CONFIG_DIR} is required but is missing or not a directory."


def test_configs_directory_contains_only_expected_files():
    present = sorted(os.listdir(CONFIG_DIR))
    expected = sorted(os.path.basename(p) for p in EXPECTED_FILES)
    assert present == expected, (
        "The following files are expected in "
        f"{CONFIG_DIR}:\n    {expected}\n"
        f"but the actual directory contents are:\n    {present}"
    )


@pytest.mark.parametrize("path, expected_content", EXPECTED_FILES.items())
def test_each_config_file_matches_ground_truth(path, expected_content):
    actual = read_file(path)
    assert (
        actual == expected_content
    ), f"File content mismatch for {path}.\nExpected bytes:\n{expected_content!r}\nGot:\n{actual!r}"


def test_output_and_clean_configs_do_not_yet_exist():
    """
    The assignment requires the student to *create* these directories.
    At the initial state they should not exist.
    """
    for d in (OUTPUT_DIR, CLEAN_DIR):
        assert not os.path.exists(
            d
        ), f"Directory {d} should not exist before the student's solution runs."


def test_config_dir_permissions_are_reasonable():
    """Optional sanity-check: directory should be readable and executable."""
    st = os.stat(CONFIG_DIR)
    assert bool(st.st_mode & stat.S_IRUSR), f"{CONFIG_DIR} is not readable by user."
    assert bool(st.st_mode & stat.S_IXUSR), f"{CONFIG_DIR} is not accessible (no +x)."