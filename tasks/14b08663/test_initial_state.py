# test_initial_state.py
#
# Pytest test-suite that validates the *initial* state of the sandbox
# before the student script is executed.

import os
import re
from pathlib import Path

import pytest

# ---------- CONSTANTS ---------- #
LOG_FILE = Path("/home/user/logs/server.log")

ANALYSIS_DIR = Path("/home/user/analysis")
EXPECTED_OUTPUTS = [
    ANALYSIS_DIR / "level_counts.txt",
    ANALYSIS_DIR / "response_stats.csv",
    ANALYSIS_DIR / "errors_filtered.log",
    ANALYSIS_DIR / "server_redacted.log",
]

ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}
ALLOWED_COMPONENTS = {"API", "AUTH", "FRONTEND"}

# ---------- HELPER REGEX ---------- #
IPV4_RE = re.compile(
    r"^(?:"
    r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)"
    r"$"
)
# Splits on literal " | " (space-pipe-space) only.
PIPE_SPLIT_RE = re.compile(r" \| ")


# ---------- TESTS ---------- #
def test_log_file_exists_and_non_empty():
    """The consolidated log must exist and be non-empty."""
    assert LOG_FILE.exists(), f"Required log file not found at: {LOG_FILE}"
    assert LOG_FILE.is_file(), f"Expected {LOG_FILE} to be a regular file."
    size = LOG_FILE.stat().st_size
    assert size > 0, f"{LOG_FILE} exists but is empty."


def test_log_lines_format_correct():
    """
    Every line must follow:
        YYYY-MM-DDThh:mm:ssZ | LEVEL | COMPONENT | IPv4 | ...<INT>ms\n
    We validate LEVEL, COMPONENT, IPv4 format, single final 'INTms',
    and that ' | ' delimiters appear exactly four times.
    """
    bad_lines = []

    with LOG_FILE.open("r", encoding="utf-8") as fh:
        for idx, raw in enumerate(fh, start=1):
            # Basic newline check
            assert raw.endswith(
                "\n"
            ), f"Line {idx} in {LOG_FILE} must end with UNIX newline '\\n'."

            # Ensure exactly four ' | ' delimiters, which produce five fields
            parts = PIPE_SPLIT_RE.split(raw.rstrip("\n"))
            if len(parts) != 5:
                bad_lines.append((idx, "delimiter count", raw))
                continue

            _ts, level, component, ip, rest = parts

            # Check LEVEL
            if level not in ALLOWED_LEVELS:
                bad_lines.append((idx, "invalid LEVEL", raw))

            # Check COMPONENT
            if component not in ALLOWED_COMPONENTS:
                bad_lines.append((idx, "invalid COMPONENT", raw))

            # Check IPv4 format
            if not IPV4_RE.match(ip):
                bad_lines.append((idx, "invalid IPv4", raw))

            # Final '<INT>ms' token at end and it must be unique
            ms_matches = re.findall(r"(\d+)ms", rest)
            if len(ms_matches) != 1 or not rest.endswith(f"{ms_matches[0]}ms"):
                bad_lines.append((idx, "duration token", raw))

    assert (
        not bad_lines
    ), "The following lines are malformed:\n" + "\n".join(
        f"Line {idx} ({reason}): {text.rstrip()}" for idx, reason, text in bad_lines
    )


def test_analysis_outputs_not_present_yet():
    """
    The artefact directory and its files should NOT exist yet.
    This guarantees the student hasn’t pre-generated any output.
    """
    if ANALYSIS_DIR.exists():
        assert (
            ANALYSIS_DIR.is_dir()
        ), f"{ANALYSIS_DIR} exists but is not a directory."
        existing = [p for p in EXPECTED_OUTPUTS if p.exists()]
        assert (
            not existing
        ), f"Output files already present before processing: {', '.join(map(str, existing))}"
    else:
        # Directory itself is absent, which is acceptable
        assert not ANALYSIS_DIR.exists(), (
            f"{ANALYSIS_DIR} should not pre-exist; "
            "student code is expected to create it."
        )