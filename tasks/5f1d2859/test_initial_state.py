# test_initial_state.py
"""
Pytest suite that validates the initial on-disk state before the student
performs any actions.  It deliberately checks ONLY the prerequisites and
avoids asserting anything about the files that the student is expected
to create or modify later on.

Requirements being verified (initial truth):
1. The directory /home/user/netops/ exists and is a directory.
2. The file /home/user/netops/interfaces.cfg exists.
3. That file contains exactly three lines:
      interface=eth0
      mtu=1500
      state=up
   with a single trailing newline and no extra whitespace.
4. No other regular files are present inside /home/user/netops/
   (directories and hidden dot-files are ignored).
"""

import os
from pathlib import Path

NETOPS_DIR = Path("/home/user/netops")
INTERFACE_CFG = NETOPS_DIR / "interfaces.cfg"

EXPECTED_LINES = [
    "interface=eth0",
    "mtu=1500",
    "state=up",
]


def _read_file_lines(path: Path):
    """
    Helper that reads the file in text mode and returns a list of lines
    stripped from their trailing newline characters. It also ensures the
    file ends with exactly one newline.
    """
    with path.open("r", encoding="utf-8") as fh:
        content = fh.read()

    # Fail if the file does not end with exactly one newline
    assert content.endswith(
        "\n"
    ), f"{path} must end with a single newline character"

    # Remove the trailing newline then split for comparisons
    return content[:-1].split("\n")


def test_netops_directory_exists_and_type():
    assert NETOPS_DIR.exists(), "Required directory /home/user/netops/ is missing"
    assert NETOPS_DIR.is_dir(), "/home/user/netops/ exists but is not a directory"


def test_interfaces_cfg_exists():
    assert INTERFACE_CFG.exists(), (
        "Required file /home/user/netops/interfaces.cfg is missing"
    )
    assert INTERFACE_CFG.is_file(), (
        "/home/user/netops/interfaces.cfg exists but is not a regular file"
    )


def test_interfaces_cfg_content():
    lines = _read_file_lines(INTERFACE_CFG)
    assert (
        lines == EXPECTED_LINES
    ), (
        "/home/user/netops/interfaces.cfg has unexpected contents\n"
        f"Expected lines:\n{EXPECTED_LINES!r}\n"
        f"Found lines:\n{lines!r}"
    )


def test_no_extra_files_in_netops():
    regular_files = [
        p.name
        for p in NETOPS_DIR.iterdir()
        if p.is_file() and p.name != INTERFACE_CFG.name
    ]
    assert (
        not regular_files
    ), (
        "Unexpected additional regular files present in /home/user/netops/: "
        f"{regular_files}"
    )