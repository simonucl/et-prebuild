# test_initial_state.py
"""
Pytest suite that verifies the initial state of the container **before**
the student performs any actions.

We check only the *input* artifacts that must be present.  We deliberately do
NOT look for (or at) the output file that the student will create later.

Expectations:
1. Directory  /home/user/logs               must exist and be a directory.
2. File       /home/user/logs/webapp.log    must exist, be readable, and
   contain exactly 10 lines.
3. Every line must contain a `response_time=<number>ms` token where <number>
   is an integer.
4. The total count of such response-time values must be 10 and their sum must
   equal 1230, which implies an average of 123.0 ms.

If any of these invariants is violated the test will fail with an explanatory
message.
"""

import re
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "webapp.log"

RESPONSE_RE = re.compile(r"\bresponse_time=(\d+)ms\b")


def test_log_directory_exists():
    assert LOG_DIR.exists(), f"Required directory not found: {LOG_DIR}"
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory."


def test_log_file_exists():
    assert LOG_FILE.exists(), f"Required log file not found: {LOG_FILE}"
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_log_file_contents():
    contents = LOG_FILE.read_text(encoding="utf-8").splitlines()
    assert (
        len(contents) == 10
    ), f"{LOG_FILE} should contain exactly 10 lines, found {len(contents)}."

    total_times = []
    for idx, line in enumerate(contents, start=1):
        match = RESPONSE_RE.search(line)
        assert (
            match
        ), f"Line {idx} in {LOG_FILE} is missing a valid 'response_time=<num>ms' token:\n{line!r}"
        total_times.append(int(match.group(1)))

    assert (
        len(total_times) == 10
    ), "Expected 10 response_time tokens (one per line)."

    sum_times = sum(total_times)
    assert (
        sum_times == 1230
    ), f"Sum of response times expected to be 1230 ms, got {sum_times} ms instead."

    avg_time = sum_times / len(total_times)
    assert (
        abs(avg_time - 123.0) < 1e-9
    ), f"Average response time expected to be 123.0 ms, got {avg_time:.1f} ms instead."