# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state that must be
# present **before** the learner starts working on the task.  It makes sure
# the two required raw log files are the only occupants of
# /home/user/workflow_logs/ and that their contents match the specification.
#
# Only the Python standard library and pytest are used.

import os
import textwrap
import pytest

WORKFLOW_DIR = "/home/user/workflow_logs"
APP_LOG      = os.path.join(WORKFLOW_DIR, "app.log")
ACCESS_LOG   = os.path.join(WORKFLOW_DIR, "access.log")

# Expected, canonical contents of the two log files (no CR characters, LF-only)
EXPECTED_APP_LOG = [
    "2023-08-01 09:15:04,123 INFO  Workflow started by user=alice id=WF1001",
    "2023-08-01 09:16:10,456 ERROR Step 1 failed with code=E42",
    "2023-08-01 09:16:20,789 INFO  Retrying step 1 attempt=2",
    "2023-08-01 09:16:25,012 ERROR Step 1 failed with code=E42",
    "2023-08-01 10:03:55,334 INFO  Workflow resumed id=WF1001",
    "2023-08-01 10:04:12,667 ERROR Step 2 failed with code=E17",
    "2023-08-01 11:22:33,890 WARNING Deprecated API used by user=bob",
    "2023-08-01 11:45:01,101 ERROR Step 3 failed with code=E99",
]

EXPECTED_ACCESS_LOG = [
    '192.168.0.11 - - [01/Aug/2023:09:15:04 +0000] "POST /api/workflow HTTP/1.1" 200 523',
    '192.168.0.11 - - [01/Aug/2023:09:16:10 +0000] "GET /api/workflow/step1 HTTP/1.1" 500 214',
    '172.16.4.15 - - [01/Aug/2023:09:16:25 +0000] "GET /api/workflow/step1 HTTP/1.1" 500 214',
    '192.168.0.11 - - [01/Aug/2023:10:04:12 +0000] "GET /api/workflow/step2 HTTP/1.1" 500 214',
    '10.0.0.5     - - [01/Aug/2023:11:45:01 +0000] "GET /api/workflow/step3 HTTP/1.1" 500 214',
    '172.16.4.15 - - [01/Aug/2023:11:45:02 +0000] "GET /favicon.ico HTTP/1.1" 404 88',
]


def _read_lines(path):
    """Return lines with universal newlines turned off to preserve exactness."""
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read().splitlines()


def test_workflow_log_directory_exists_and_is_directory():
    assert os.path.isdir(WORKFLOW_DIR), (
        f"Expected directory {WORKFLOW_DIR!r} to exist but it is missing."
    )


def test_required_log_files_exist():
    missing = [p for p in (APP_LOG, ACCESS_LOG) if not os.path.isfile(p)]
    assert not missing, (
        "The following required log files are missing:\n"
        + "\n".join(missing)
    )


def test_no_extra_files_in_workflow_logs():
    expected = {"app.log", "access.log"}
    actual   = set(os.listdir(WORKFLOW_DIR))
    extra    = actual - expected
    missing  = expected - actual
    assert not extra and not missing, textwrap.dedent(
        f"""\
        Directory {WORKFLOW_DIR} must contain exactly the two files
        {', '.join(sorted(expected))}.
        Extra files   : {', '.join(sorted(extra))   or 'None'}
        Missing files : {', '.join(sorted(missing)) or 'None'}
        """
    )


@pytest.mark.parametrize(
    "path, expected_lines",
    [
        (APP_LOG, EXPECTED_APP_LOG),
        (ACCESS_LOG, EXPECTED_ACCESS_LOG),
    ],
)
def test_log_file_contents_are_exact(path, expected_lines):
    lines = _read_lines(path)
    assert lines == expected_lines, textwrap.dedent(
        f"""\
        File {path} does not match the expected canonical content.
        Expected {len(expected_lines)} lines, found {len(lines)}.
        First difference (if any) shown below:
        EXPECTED: {next((l for l in expected_lines if l not in lines), '<none>')}
        FOUND   : {next((l for l in lines if l not in expected_lines), '<none>')}
        """
    )


@pytest.mark.parametrize("path", [APP_LOG, ACCESS_LOG])
def test_files_use_unix_line_endings_only(path):
    with open(path, "rb") as fh:
        content = fh.read()
    assert b"\r" not in content, (
        f"{path} contains carriage-return characters (CR, '\\r'). "
        "Files must use Unix LF line endings only."
    )