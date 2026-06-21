# test_initial_state.py
#
# Pytest suite that validates the *initial* OS / filesystem state
# before the student executes any commands.  It confirms that the
# required input files and directories exist and that their contents
# are *exactly* as specified in the task description.
#
# NOTE: The tests intentionally avoid touching / validating anything
# under /home/user/provisioning/output/ as per the grading rules.

import pathlib
import pytest

# Base paths
BASE_DIR = pathlib.Path("/home/user/provisioning")
INPUT_DIR = BASE_DIR / "input"

# Expected file paths
SERVERS_CSV = INPUT_DIR / "servers.csv"
NETWORK_CSV = INPUT_DIR / "network.csv"


@pytest.mark.parametrize(
    "path, is_dir",
    [
        (BASE_DIR, True),
        (INPUT_DIR, True),
        (SERVERS_CSV, False),
        (NETWORK_CSV, False),
    ],
)
def test_paths_exist(path: pathlib.Path, is_dir: bool) -> None:
    """
    Ensure required directories and files exist before the workflow starts.
    """
    assert path.exists(), f"Required {'directory' if is_dir else 'file'} not found: {path}"
    if is_dir:
        assert path.is_dir(), f"Expected directory but found something else: {path}"
    else:
        assert path.is_file(), f"Expected regular file but found something else: {path}"


def _read_text(path: pathlib.Path) -> str:
    """
    Read a text file using UTF-8 encoding, preserving newlines verbatim.
    """
    return path.read_text(encoding="utf-8")


def test_servers_csv_exact_content() -> None:
    """
    /home/user/provisioning/input/servers.csv must match the task description
    byte-for-byte (UTF-8 text).
    """
    expected = (
        "host,ip,cpu,ram\n"
        "web01,10.10.1.11,4,16\n"
        "db01,10.10.1.12,8,32\n"
        "cache01,10.10.1.13,2,8\n"
    )
    actual = _read_text(SERVERS_CSV)
    assert (
        actual == expected
    ), f"servers.csv content mismatch.\nExpected:\n{expected!r}\nGot:\n{actual!r}"


def test_network_csv_exact_content() -> None:
    """
    /home/user/provisioning/input/network.csv must match the task description
    byte-for-byte (UTF-8 text).
    """
    expected = (
        "ip,vlan,subnet\n"
        "10.10.1.11,frontend,10.10.1.0/24\n"
        "10.10.1.12,backend,10.10.1.0/24\n"
        "10.10.1.13,cache,10.10.1.0/24\n"
    )
    actual = _read_text(NETWORK_CSV)
    assert (
        actual == expected
    ), f"network.csv content mismatch.\nExpected:\n{expected!r}\nGot:\n{actual!r}"