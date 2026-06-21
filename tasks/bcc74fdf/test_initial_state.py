# test_initial_state.py
#
# This pytest suite validates that the expected *initial* filesystem state
# is present before the student begins working on the assignment.
#
# It intentionally does NOT check for the existence of any output artefacts
# (e.g. /home/user/profiler/combined_profile.tsv); it only verifies the
# presence and exact contents of the provided input snapshots.

import difflib
from pathlib import Path

import pytest

HOME = Path("/home/user")
PROFILER_DIR = HOME / "profiler"
CPU_LOG = PROFILER_DIR / "cpu.log"
MEM_LOG = PROFILER_DIR / "mem.log"


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (HOME, "home directory"),
        (PROFILER_DIR, "profiler directory"),
    ],
)
def test_directories_exist(path_obj: Path, description: str) -> None:
    assert path_obj.exists(), f"Required {description} '{path_obj}' is missing."
    assert path_obj.is_dir(), f"'{path_obj}' should be a directory."


def read_bytes(path_: Path) -> bytes:
    """
    Helper that returns the full byte sequence of a file.

    Reading as *bytes* avoids any accidental newline or encoding conversion
    that could mask formatting errors the student must preserve.
    """
    return path_.read_bytes()


def assert_file_exact(path_: Path, expected: bytes) -> None:
    """Assert that a file exists and its byte-for-byte content matches."""
    assert path_.exists(), f"Expected file '{path_}' does not exist."
    assert path_.is_file(), f"'{path_}' should be a regular file (not a directory)."

    actual = read_bytes(path_)
    if actual != expected:
        # Produce a readable unified diff to aid debugging.
        diff = "\n".join(
            difflib.unified_diff(
                expected.decode().splitlines(),
                actual.decode().splitlines(),
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
        )
        pytest.fail(
            f"Contents of '{path_}' do not match the required initial snapshot.\n"
            f"--- Expected vs. Actual ---\n{diff}"
        )


def test_cpu_log_contents() -> None:
    expected_cpu = (
        b"PID\tCommand\tCPU%\n"
        b"101\tnginx\t12.3\n"
        b"202\tpostgres\t43.1\n"
        b"303\tredis\t5.6\n"
    )
    assert_file_exact(CPU_LOG, expected_cpu)


def test_mem_log_contents() -> None:
    expected_mem = (
        b"PID\tCommand\tMEM%\n"
        b"101\tnginx\t84\n"
        b"202\tpostgres\t256\n"
        b"303\tredis\t37\n"
    )
    assert_file_exact(MEM_LOG, expected_mem)