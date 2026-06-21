# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student performs any action.  It checks that the legacy tools
# and sample data are present and correct, and that the required output
# artefact has **not** been created yet.

import os
import subprocess
from pathlib import Path

LEGACY_DIR = Path("/home/user/legacy_tools")
WORD_COUNT_SCRIPT = LEGACY_DIR / "word_count.sh"
SAMPLE_TXT = LEGACY_DIR / "sample.txt"

OUTPUT_DIR = Path("/home/user/output")
OUTPUT_LOG = OUTPUT_DIR / "sample_wc.log"


def test_legacy_directory_exists():
    assert LEGACY_DIR.is_dir(), (
        f"Expected legacy tools directory {LEGACY_DIR} to exist. "
        "It is missing."
    )


def test_word_count_script_exists_and_executable():
    assert WORD_COUNT_SCRIPT.is_file(), (
        f"Expected script {WORD_COUNT_SCRIPT} to be a regular file. "
        "It is missing."
    )
    # Verify the script is executable for the current user.
    is_executable = os.access(WORD_COUNT_SCRIPT, os.X_OK)
    assert is_executable, (
        f"Script {WORD_COUNT_SCRIPT} is not marked as executable. "
        "Add execute permissions (chmod +x)."
    )


def test_sample_txt_exists_with_expected_content():
    assert SAMPLE_TXT.is_file(), (
        f"Sample text file {SAMPLE_TXT} is missing."
    )

    # We expect the file to contain exactly six words: "Hello world from legacy code base."
    # That makes 6 whitespace-separated tokens.
    content = SAMPLE_TXT.read_text(encoding="utf-8").strip()
    word_count = len(content.split())
    assert word_count == 6, (
        f"Expected {SAMPLE_TXT} to contain 6 words, "
        f"but found {word_count}. File contents may have been modified."
    )


def test_word_count_script_outputs_correct_number():
    """Run the shell script and verify it prints '6' and exits with status 0."""
    result = subprocess.run(
        ["/bin/sh", str(WORD_COUNT_SCRIPT), str(SAMPLE_TXT)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"{WORD_COUNT_SCRIPT} exited with status {result.returncode}, "
        "expected 0."
    )

    # Allow an optional trailing newline from the shell script.
    output = result.stdout
    stripped_output = output.strip()

    assert stripped_output == "6", (
        f"{WORD_COUNT_SCRIPT} reported '{output!r}' when run against "
        f"{SAMPLE_TXT}. Expected the integer '6' (optionally followed by a "
        "newline)."
    )


def test_output_log_does_not_exist_yet():
    """
    The student is supposed to create /home/user/output/sample_wc.log.
    At the initial state this artifact **must not exist**.
    """
    assert not OUTPUT_LOG.exists(), (
        f"Output log {OUTPUT_LOG} already exists. "
        "The initial state should not include this file."
    )