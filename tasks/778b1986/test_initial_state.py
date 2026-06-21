# test_initial_state.py
#
# Pytest suite that validates the initial state of the operating system
# before the student generates any reports.  It checks only the presence
# and exact contents of the raw deployment log files, *not* the output
# directory or report files that the student will create later.

import re
from pathlib import Path

LOG_DIR = Path("/home/user/deployment/logs").expanduser()

EXPECTED_LOG_FILES = {
    LOG_DIR / "2023-09-01.log": [
        "2023-09-01 02:15:12 [web-01] STATUS: OK",
        "2023-09-01 02:16:05 [db-01] STATUS: FAIL",
        "2023-09-01 02:17:45 [cache-01] STATUS: OK",
        "2023-09-01 02:18:20 [auth-01] STATUS: FAIL",
    ],
    LOG_DIR / "2023-09-02.log": [
        "2023-09-02 02:14:02 [web-02] STATUS: OK",
        "2023-09-02 02:15:47 [db-02] STATUS: OK",
        "2023-09-02 02:16:37 [cache-02] STATUS: OK",
        "2023-09-02 02:18:55 [auth-02] STATUS: OK",
    ],
    LOG_DIR / "2023-09-03.log": [
        "2023-09-03 02:13:33 [web-03] STATUS: OK",
        "2023-09-03 02:15:02 [db-03] STATUS: FAIL",
        "2023-09-03 02:16:58 [cache-03] STATUS: FAIL",
        "2023-09-03 02:17:42 [auth-03] STATUS: OK",
    ],
}

LINE_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2} "        # Date YYYY-MM-DD
    r"\d{2}:\d{2}:\d{2} "         # Time HH:MM:SS
    r"\[[^\[\]]+\] "              # [server-name]
    r"STATUS: (OK|FAIL)$"         # STATUS: OK|FAIL
)

def test_log_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Expected log directory '{LOG_DIR}' to exist and be a directory."
    )

def test_expected_log_files_exist():
    for path in EXPECTED_LOG_FILES:
        assert path.is_file(), (
            f"Expected log file '{path}' to exist and be a regular file."
        )

def test_no_extra_log_files():
    actual_logs = sorted(p for p in LOG_DIR.glob("*.log") if p.is_file())
    expected_logs = sorted(EXPECTED_LOG_FILES.keys())
    assert actual_logs == expected_logs, (
        "The log directory contains unexpected .log files.\n"
        f"Expected exactly:\n  " + "\n  ".join(str(p) for p in expected_logs) +
        "\nBut found:\n  " + "\n  ".join(str(p) for p in actual_logs)
    )

def _read_file_lines(path: Path):
    # Read file and strip only the trailing newline from each line,
    # preserving any internal spaces.
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]

def test_log_file_contents_exact_match():
    for path, expected_lines in EXPECTED_LOG_FILES.items():
        actual_lines = _read_file_lines(path)
        assert actual_lines == expected_lines, (
            f"Contents of '{path}' do not match the expected lines.\n"
            f"Expected ({len(expected_lines)} lines):\n  " +
            "\n  ".join(expected_lines) +
            f"\n\nActual ({len(actual_lines)} lines):\n  " +
            "\n  ".join(actual_lines)
        )

def test_each_line_conforms_to_expected_pattern():
    for path in EXPECTED_LOG_FILES:
        for lineno, line in enumerate(_read_file_lines(path), start=1):
            assert LINE_PATTERN.match(line), (
                f"Line {lineno} in '{path}' does not conform to the required "
                "format 'YYYY-MM-DD HH:MM:SS [server-name] STATUS: OK|FAIL'.\n"
                f"Offending line: {line}"
            )