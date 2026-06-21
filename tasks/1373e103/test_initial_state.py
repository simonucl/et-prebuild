# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state **before** the student
performs any action for the “failure_job_ids” aggregation task.

This file checks only the pre-existing artifacts that must be present:
  • /home/user/logs directory
  • /home/user/logs/node1.log with the exact expected content
  • /home/user/logs/node2.log with the exact expected content

Per the grading rules **we intentionally do NOT test for the presence or
absence of /home/user/output or any files therein**, because those are the
artifacts the student is supposed to create.
"""

import pathlib
import textwrap
import pytest

HOME_DIR = pathlib.Path("/home/user")
LOGS_DIR = HOME_DIR / "logs"
NODE1_LOG = LOGS_DIR / "node1.log"
NODE2_LOG = LOGS_DIR / "node2.log"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #


def _normalise_multiline(multiline: str):
    """
    Drop leading indentation that might be introduced by the triple-quoted
    string formatting used below.
    """
    return textwrap.dedent(multiline).lstrip("\n").rstrip()  # noqa: E501


def _read_file(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}", pytrace=False)  # noqa: E501


# --------------------------------------------------------------------------- #
# Expected file contents (trailing newline included)
# --------------------------------------------------------------------------- #

EXPECTED_NODE1_CONTENT = _normalise_multiline(
    """
    2023-12-01T10:15:30Z INFO  node1 1001 Task started
    2023-12-01T10:16:00Z ERROR node1 1001 OutOfMemory
    2023-12-01T10:17:00Z INFO  node1 1002 Task started
    2023-12-01T10:17:30Z ERROR node1 1002 Timeout
    """
) + "\n"

EXPECTED_NODE2_CONTENT = _normalise_multiline(
    """
    2023-12-01T10:20:10Z INFO  node2 2001 Task started
    2023-12-01T10:21:00Z ERROR node2 2001 DiskFull
    2023-12-01T10:22:00Z INFO  node2 2002 Task started
    2023-12-01T10:22:30Z INFO  node2 2002 Task finished successfully
    2023-12-01T10:23:00Z ERROR node2 2003 NetworkPartition
    """
) + "\n"

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_home_directory_exists():
    assert HOME_DIR.is_dir(), (
        f"Expected home directory {HOME_DIR} to exist, "
        "but it is missing."
    )


def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), (
        f"Expected logs directory {LOGS_DIR} to exist, "
        "but it is missing."
    )


@pytest.mark.parametrize(
    "path_, expected_content",
    [
        (NODE1_LOG, EXPECTED_NODE1_CONTENT),
        (NODE2_LOG, EXPECTED_NODE2_CONTENT),
    ],
)
def test_log_file_exists_and_has_expected_content(path_: pathlib.Path, expected_content: str):
    assert path_.is_file(), f"Required log file {path_} is missing."

    actual_content = _read_file(path_)

    # Verify the content matches exactly.
    if actual_content != expected_content:
        # Provide a concise but clear diff-style message.
        expected_lines = expected_content.splitlines(keepends=True)
        actual_lines = actual_content.splitlines(keepends=True)
        diff_lines = [
            f"- {exp.rstrip()}" for exp in expected_lines if exp not in actual_lines
        ] + [
            f"+ {act.rstrip()}" for act in actual_lines if act not in expected_lines
        ]
        diff_preview = "\n".join(diff_lines[:10])  # Show at most first 10 differences
        pytest.fail(
            f"Content of {path_} does not match expected content.\n"
            f"First differing lines (prefix '-' = expected, '+' = actual):\n"
            f"{diff_preview}"
        )