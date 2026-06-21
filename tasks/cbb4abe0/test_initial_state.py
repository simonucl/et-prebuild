# test_initial_state.py
#
# Pytest suite that validates the *initial* (pre-graded) state of the
# operating system / file-system for the “echo” web-service exercise.
#
# Rules / expectations (all must be met **exactly**):
# 1. Directory            : /home/user/qa_echo
# 2. Config file          : /home/user/qa_echo/echo.env
#    Exact 3-line content :
#        ECHO_PORT=9090
#        ECHO_MODE=testing
#        ECHO_TIMEOUT=5
# 3. Bash alias           : last line of /home/user/.bashrc is exactly
#        alias echo-test="python3 -m http.server 9090 --directory /home/user/qa_echo"
#    …and there are no lines after it.
# 4. Verification log     : /home/user/qa_echo/setup.log
#    Exact 4-line YAML block
#        setup:
#          config_file: "/home/user/qa_echo/echo.env"
#          bash_alias_added: "yes"
#          status: "ok"
#
# All checks are byte-for-byte unless otherwise stated.
# Only stdlib + pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")
QA_DIR = HOME / "qa_echo"
CONFIG_FILE = QA_DIR / "echo.env"
BASHRC = HOME / ".bashrc"
SETUP_LOG = QA_DIR / "setup.log"

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def read_bytes(path: Path) -> bytes:
    """Return the full byte content of the file, raising a helpful
    assertion message if the file is unreadable.
    """
    assert path.exists(), f"Expected file {path} does not exist."
    try:
        return path.read_bytes()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_directory_exists():
    assert QA_DIR.is_dir(), f"Directory {QA_DIR} is missing."


def test_echo_env_exact_contents():
    expected_lines = [
        "ECHO_PORT=9090",
        "ECHO_MODE=testing",
        "ECHO_TIMEOUT=5",
    ]

    content_bytes = read_bytes(CONFIG_FILE)
    content_text = content_bytes.decode("utf-8")

    # Split lines WITHOUT keeping newline chars; this tolerates
    # a trailing newline but forbids an extra *blank* line.
    actual_lines = content_text.splitlines()
    assert (
        actual_lines == expected_lines
    ), f"{CONFIG_FILE} contents are incorrect.\nExpected lines:\n{expected_lines}\nActual lines:\n{actual_lines}"


def test_bashrc_ends_with_correct_alias():
    alias_line = (
        'alias echo-test="python3 -m http.server 9090 --directory /home/user/qa_echo"'
    )

    bashrc_text = read_bytes(BASHRC).decode("utf-8")
    lines = bashrc_text.splitlines()

    assert lines, f"{BASHRC} is empty; expected at least the alias line."

    last_line = lines[-1]
    assert (
        last_line == alias_line
    ), f'Last line of {BASHRC!s} is incorrect.\nExpected: {alias_line!r}\nGot     : {last_line!r}'

    # Ensure *no* blank lines follow the alias (splitlines() drops final newline,
    # so we just need to make sure there wasn’t an extra blank line).
    assert (
        "" not in lines[-1:]
    ), f"{BASHRC} must not contain blank lines after the alias line."


def test_setup_log_exact_bytes():
    expected_log = (
        "setup:\n"
        '  config_file: "/home/user/qa_echo/echo.env"\n'
        '  bash_alias_added: "yes"\n'
        '  status: "ok"\n'
    ).encode("utf-8")

    actual_log = read_bytes(SETUP_LOG)
    assert (
        actual_log == expected_log
    ), f"{SETUP_LOG} does not match expected content.\n\nExpected bytes:\n{expected_log!r}\n\nActual bytes:\n{actual_log!r}"