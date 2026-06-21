# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be present
# before the student begins work.  It intentionally makes **no reference** to
# any of the artefacts that the student will later create (e.g. the
# /home/user/diagnostics directory or its contents).  If any of these tests
# fail, the exercise environment itself is broken – not the student’s code.

import re
from pathlib import Path

import pytest

HOME = Path("/home/user")
MS_ROOT = HOME / "microservices"

# --------------------------------------------------------------------------- #
# Helpers & expected data
# --------------------------------------------------------------------------- #
SERVICE_INFO = {
    "service-a": {
        "line_count": 10,
        "lines": [
            "2024-06-20T09:00:01Z INFO [c142] latency=120 status=200",
            "2024-06-20T09:00:02Z INFO [c143] latency=110 status=200",
            "2024-06-20T09:00:03Z INFO [c144] latency=130 status=200",
            "2024-06-20T09:00:04Z INFO [c145] latency=125 status=200",
            "2024-06-20T09:00:05Z INFO [c146] latency=140 status=200",
            "2024-06-20T09:00:06Z INFO [c147] latency=115 status=200",
            "2024-06-20T09:00:07Z INFO [c148] latency=118 status=200",
            "2024-06-20T09:00:08Z INFO [c149] latency=121 status=200",
            "2024-06-20T09:00:09Z ERROR [c150] latency=119 status=500",
            "2024-06-20T09:00:10Z INFO [c151] latency=117 status=200",
        ],
    },
    "service-b": {
        "line_count": 6,
        "lines": [
            "2024-06-20T09:00:11Z INFO [d242] latency=100 status=200",
            "2024-06-20T09:00:12Z INFO [d243] latency=102 status=200",
            "2024-06-20T09:00:13Z INFO [d244] latency=98  status=200".replace(
                "  ", " "
            ),
            "2024-06-20T09:00:14Z INFO [d245] latency=97 status=200",
            "2024-06-20T09:00:15Z INFO [d246] latency=101 status=200",
            "2024-06-20T09:00:16Z INFO [d247] latency=99 status=200",
        ],
    },
    "service-c": {
        "line_count": 4,
        "lines": [
            "2024-06-20T09:00:17Z INFO [e342] latency=210 status=200",
            "2024-06-20T09:00:18Z INFO [e343] latency=230 status=200",
            "2024-06-20T09:00:19Z ERROR [e344] latency=220 status=503",
            "2024-06-20T09:00:20Z INFO [e345] latency=215 status=200",
        ],
    },
}

LOG_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z "
    r"(INFO|ERROR) "
    r"\[[a-z0-9]+\] "
    r"latency=\d+ "
    r"status=\d{3}$"
)

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("service", SERVICE_INFO.keys())
def test_service_directory_exists(service):
    path = MS_ROOT / service
    assert path.is_dir(), (
        f"Expected directory {path} to exist "
        "but it is missing or not a directory."
    )


@pytest.mark.parametrize("service", SERVICE_INFO.keys())
def test_logs_subdirectory_exists(service):
    path = MS_ROOT / service / "logs"
    assert path.is_dir(), (
        f"Expected logs subdirectory {path} to exist "
        "but it is missing or not a directory."
    )


@pytest.mark.parametrize("service", SERVICE_INFO.keys())
def test_app_log_file_exists(service):
    path = MS_ROOT / service / "logs" / "app.log"
    assert path.is_file(), f"Expected log file {path} to exist but it is missing."


@pytest.mark.parametrize("service,info", SERVICE_INFO.items())
def test_app_log_contents(service, info):
    """Validate exact number of lines, each line's format, and its content."""
    file_path = MS_ROOT / service / "logs" / "app.log"
    lines = file_path.read_text(encoding="utf-8").splitlines()
    # Check line count
    assert (
        len(lines) == info["line_count"]
    ), f"{file_path} should contain {info['line_count']} lines, found {len(lines)}."
    # Check line-by-line exact match
    assert (
        lines == info["lines"]
    ), f"Contents of {file_path} do not match the expected snapshot."
    # Validate regex format for every line
    for lineno, line in enumerate(lines, 1):
        assert LOG_RE.match(
            line
        ), f"Line {lineno} in {file_path} has unexpected format: {line!r}"