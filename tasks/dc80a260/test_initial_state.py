# test_initial_state.py
#
# Pytest suite to verify the pristine state of the operating-system / filesystem
# *before* the student performs the hardening tasks described in the assignment.
#
# The tests assert that:
#   • The two baseline configuration files and their parent directories exist
#     with the correct permissions and *exact* contents.
#   • No artefacts that the student is supposed to create during the task
#     (/home/user/hardening_workshop, tarball, hardened files, summary log, …)
#     are present yet.
#
# Any deviation from these expectations will cause a test failure with a clear
# explanatory message.

import os
import stat
import glob
import datetime
import pytest

HOME = "/home/user"

# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def mode(path):
    """Return the permission bits of a filesystem object as an int, e.g. 0o644"""
    return stat.S_IMODE(os.lstat(path).st_mode)


def assert_file_mode(path, expected):
    assert mode(path) == expected, (
        f"Permissions for {path} are {oct(mode(path))}, expected {oct(expected)}"
    )


def assert_dir_mode(path, expected):
    # Same helper but with a directory-specific error message
    assert mode(path) == expected, (
        f"Permissions for directory {path} are {oct(mode(path))}, "
        f"expected {oct(expected)}"
    )


def assert_not_exists(path):
    assert not os.path.exists(path), f"{path} should NOT exist before the task starts"


# --------------------------------------------------------------------------- #
# Expected baseline file data                                                 #
# --------------------------------------------------------------------------- #
BASELINE_FILES = {
    f"{HOME}/baseline_configs/ssh/sshd_config_baseline": [
        "# Baseline SSH config\n",
        "Port 22\n",
        "Protocol 2\n",
        "HostKey /etc/ssh/ssh_host_rsa_key\n",
    ],
    f"{HOME}/baseline_configs/sysctl/sysctl_baseline.conf": [
        "# Baseline sysctl\n",
        "net.ipv4.ip_forward = 0\n",
        "net.ipv6.conf.all.disable_ipv6 = 1\n",
        "vm.swappiness = 10\n",
    ],
}

BASELINE_DIRS = [
    f"{HOME}/baseline_configs",
    f"{HOME}/baseline_configs/ssh",
    f"{HOME}/baseline_configs/sysctl",
]

# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("dpath", BASELINE_DIRS)
def test_baseline_directories_exist_with_correct_permissions(dpath):
    assert os.path.isdir(dpath), f"Directory {dpath} is missing"
    assert_dir_mode(dpath, 0o755)


@pytest.mark.parametrize("fpath, expected_lines", BASELINE_FILES.items())
def test_baseline_files_exist_with_correct_permissions_and_content(fpath, expected_lines):
    assert os.path.isfile(fpath), f"Baseline file {fpath} is missing"
    assert_file_mode(fpath, 0o644)

    with open(fpath, "r", encoding="utf-8") as fh:
        contents = fh.readlines()

    assert contents == expected_lines, (
        f"Contents of {fpath} do not match the expected baseline.\n"
        f"Expected:\n{''.join(expected_lines)}\n"
        f"Got:\n{''.join(contents)}"
    )

    # Ensure the file ends with a newline character
    assert contents[-1].endswith("\n"), f"The last line of {fpath} is not LF-terminated"


def test_workshop_directory_does_not_yet_exist():
    workshop_dir = f"{HOME}/hardening_workshop"
    assert_not_exists(workshop_dir)


def test_no_premature_output_artifacts():
    """
    Verify that none of the artefacts the student will create later are present.
    This includes the workshop sub-copies, the tarball, hardened files and
    the summary log.
    """
    workshop_dir = f"{HOME}/hardening_workshop"

    # If the directory is already present, bail out early with a clear message
    assert_not_exists(workshop_dir)

    # Even if the directory is absent, we still check for artefacts directly
    artefacts = [
        f"{HOME}/hardened_summary.log",
        # Hardened workshop artefacts (guard against someone creating them in HOME)
        f"{HOME}/sshd_config_baseline",
        f"{HOME}/sysctl_baseline.conf",
        f"{HOME}/sshd_config_hardened",
        f"{HOME}/sysctl_hardened.conf",
    ]
    for path in artefacts:
        assert_not_exists(path)

    # Also ensure no stray tarballs with the expected naming pattern exist
    today = datetime.datetime.utcnow().strftime("%Y%m%d")
    tarball_pattern = f"{HOME}/hardening_workshop/baseline_backup_{today}.tar.gz"
    assert len(glob.glob(tarball_pattern)) == 0, (
        f"Found an unexpected tarball matching {tarball_pattern}"
    )