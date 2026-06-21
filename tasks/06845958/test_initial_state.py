# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must
# be present before the student starts fixing the symlinks.  If any of
# these tests fail it means the starting environment is wrong and the
# exercise cannot be graded reliably.

import os
from pathlib import Path

HOME = Path("/home/user")


def _readlink(path: Path) -> str:
    """
    Helper that returns the raw target of a symlink.

    Raises:
        AssertionError if *path* is not a symlink.
    """
    assert path.is_symlink(), f"Expected {path} to be a symlink."
    return os.readlink(path)  # returns target exactly as stored (may be relative)


# --------------------------------------------------------------------------- #
# Basic directory structure                                                   #
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    netcfg = HOME / "network_configs"
    site_v1 = netcfg / "siteA_v1"
    site_v2 = netcfg / "siteA_v2"
    bin_dir = HOME / "bin"
    tools_dir = HOME / "tools"

    for d in (netcfg, site_v1, site_v2, bin_dir, tools_dir):
        assert d.is_dir(), f"Missing required directory: {d}"


# --------------------------------------------------------------------------- #
# network_configs/active symlink (should point to *siteA_v1* initially)       #
# --------------------------------------------------------------------------- #
def test_active_symlink_points_to_old_version():
    netcfg = HOME / "network_configs"
    active_link = netcfg / "active"

    assert active_link.exists() or active_link.is_symlink(), (
        f"{active_link} is missing."
    )
    assert active_link.is_symlink(), f"{active_link} is not a symlink."

    target = _readlink(active_link)
    expected_target = "siteA_v1"  # stored as a *relative* link
    assert (
        target == expected_target
    ), f"{active_link} should point to {expected_target!r}, found {target!r}."


# --------------------------------------------------------------------------- #
# network_configs/symlink_changes.log (must exist and be empty)               #
# --------------------------------------------------------------------------- #
def test_symlink_changes_log_exists_and_empty():
    log_file = HOME / "network_configs" / "symlink_changes.log"
    assert log_file.exists(), f"Missing log file: {log_file}"
    assert log_file.is_file(), f"{log_file} exists but is not a regular file."
    contents = log_file.read_text(encoding="utf-8")
    assert (
        contents == "" or contents.endswith("\n") and contents.strip() == ""
    ), (
        "symlink_changes.log should be empty at the start of the exercise; "
        "found unexpected content."
    )


# --------------------------------------------------------------------------- #
# /home/user/bin symlinks                                                     #
# --------------------------------------------------------------------------- #
def test_bin_symlinks_status():
    bin_dir = HOME / "bin"

    # ping-test: valid link to ../scripts/ping-test.sh
    ping_link = bin_dir / "ping-test"
    assert ping_link.is_symlink(), f"{ping_link} must be a symlink."
    ping_target = _readlink(ping_link)
    assert (
        ping_target == "../scripts/ping-test.sh"
    ), f"{ping_link} should point to '../scripts/ping-test.sh', found {ping_target!r}."

    # ip-test: currently broken link to ../scripts/ip-test.sh
    ip_link = bin_dir / "ip-test"
    assert ip_link.is_symlink(), f"{ip_link} must be a symlink."
    ip_target = _readlink(ip_link)
    expected_ip_target = "../scripts/ip-test.sh"
    assert (
        ip_target == expected_ip_target
    ), f"{ip_link} should point to {expected_ip_target!r}, found {ip_target!r}."

    # Verify that the link is indeed broken (the ultimate target does not exist)
    resolved = (ip_link.parent / ip_target).resolve()
    assert not resolved.exists(), (
        f"{ip_link} is expected to be broken initially, but its target "
        f"{resolved} unexpectedly exists."
    )


# --------------------------------------------------------------------------- #
# /home/user/tools/ip-test.sh must exist (the file that will become the target)
# --------------------------------------------------------------------------- #
def test_tools_ip_test_script_exists():
    script = HOME / "tools" / "ip-test.sh"
    assert script.is_file(), f"Missing helper script: {script}"
    # A very small sanity check that it looks like a shell script
    first_line = script.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.startswith("#!"), (
        f"{script} should start with a shebang, found: {first_line!r}"
    )