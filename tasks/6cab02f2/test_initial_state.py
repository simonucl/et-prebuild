# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state for the
# “certificate bundle” exercise **before** the student runs any solution
# code.  According to the task description, the directory
#   /home/user/profiling
# must not exist yet.  The presence of the directory (with or without
# content) would indicate that the student—or some previous process—has
# already started modifying the filesystem, which violates the clean-slate
# requirement.  These tests intentionally do *not* check for the final
# artefacts (profiling.key, profiling.crt, cert_info.log); they only ensure
# that nothing has been created prematurely.

import os
import stat
import pytest

HOME = "/home/user"
PROFILING_DIR = os.path.join(HOME, "profiling")
CERTS_DIR = os.path.join(PROFILING_DIR, "certs")

@pytest.fixture(scope="module")
def path_exists():
    """Utility that returns a dict with booleans for relevant paths."""
    return {
        "profiling_dir": os.path.exists(PROFILING_DIR),
        "certs_dir": os.path.exists(CERTS_DIR),
        "key_file": os.path.exists(os.path.join(CERTS_DIR, "profiling.key")),
        "crt_file": os.path.exists(os.path.join(CERTS_DIR, "profiling.crt")),
        "log_file": os.path.exists(os.path.join(CERTS_DIR, "cert_info.log")),
    }

def _fmt_permissions(path: str) -> str:
    """Return permissions of *existing* path in octal, e.g. '0o644'."""
    mode = os.stat(path).st_mode
    return oct(stat.S_IMODE(mode))

def test_profiling_directory_absent(path_exists):
    assert not path_exists["profiling_dir"], (
        f"The directory {PROFILING_DIR!r} should NOT exist at the beginning "
        f"of the exercise, but it does (permissions: "
        f"{_fmt_permissions(PROFILING_DIR) if path_exists['profiling_dir'] else 'N/A'})."
    )

def test_certs_directory_absent(path_exists):
    assert not path_exists["certs_dir"], (
        f"The directory {CERTS_DIR!r} should NOT exist yet. "
        "It will be created by the student’s solution."
    )

@pytest.mark.parametrize(
    "key",
    ["key_file", "crt_file", "log_file"],
)
def test_no_certificate_files_exist(path_exists, key):
    assert not path_exists[key], (
        "Found an unexpected file before the exercise started: "
        f"{os.path.join(CERTS_DIR, {'key_file':'profiling.key','crt_file':'profiling.crt','log_file':'cert_info.log'}[key])}"
    )