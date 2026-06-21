# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state required before the student begins their task.

import os
import stat
from pathlib import Path

DNS_DIR = Path("/home/user/dns_testset")
EXPECTED_FILE = DNS_DIR / "expected_hosts.txt"

DIR_MODE_EXPECTED = 0o755
FILE_MODE_EXPECTED = 0o644

EXPECTED_LINES = [
    "localhost=127.0.0.1",
    "ip6-localhost=::1",
]


def _mode(path: Path) -> int:
    """
    Return the permission bits (e.g., 0o644) for the given path.
    """
    return stat.S_IMODE(path.stat().st_mode)


def test_dns_directory_exists_with_correct_permissions():
    """
    Ensure /home/user/dns_testset exists and has 0755 permissions.
    """
    assert DNS_DIR.exists(), (
        f"Required directory '{DNS_DIR}' is missing."
    )
    assert DNS_DIR.is_dir(), (
        f"Expected '{DNS_DIR}' to be a directory, but it is not."
    )

    mode = _mode(DNS_DIR)
    assert mode == DIR_MODE_EXPECTED, (
        f"Directory '{DNS_DIR}' must have permissions "
        f"{oct(DIR_MODE_EXPECTED)}, found {oct(mode)}."
    )


def test_expected_hosts_file_presence_and_permissions():
    """
    Ensure expected_hosts.txt exists with mode 0644.
    """
    assert EXPECTED_FILE.exists(), (
        f"Required file '{EXPECTED_FILE}' is missing."
    )
    assert EXPECTED_FILE.is_file(), (
        f"Expected '{EXPECTED_FILE}' to be a regular file, but it is not."
    )

    mode = _mode(EXPECTED_FILE)
    assert mode == FILE_MODE_EXPECTED, (
        f"File '{EXPECTED_FILE}' must have permissions "
        f"{oct(FILE_MODE_EXPECTED)}, found {oct(mode)}."
    )


def test_expected_hosts_file_contents_exact():
    """
    Verify that expected_hosts.txt contains exactly the two required lines,
    in order, with Unix LF line endings and NO trailing newline at EOF.
    """
    # Read as binary to inspect exact line endings.
    data = EXPECTED_FILE.read_bytes()

    # Split on b'\n' – this is safe even if the last line lacks a newline.
    raw_lines = data.split(b"\n")

    # If the file ends with '\n', the last element after split would be b''.
    assert raw_lines[-1] != b"", (
        f"File '{EXPECTED_FILE}' must NOT have a trailing newline after the "
        f"second line."
    )

    decoded_lines = [line.decode("utf-8") for line in raw_lines]

    assert decoded_lines == EXPECTED_LINES, (
        f"File '{EXPECTED_FILE}' must contain exactly:\n"
        f"{EXPECTED_LINES[0]}\n{EXPECTED_LINES[1]}\n"
        f"Found:\n" + "\n".join(decoded_lines)
    )