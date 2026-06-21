# test_initial_state.py
#
# This pytest file validates the **initial** state of the filesystem
# before the student carries out any actions.  It checks only the
# prerequisites (input artefacts) and purposefully ignores every file
# or directory that the student is expected to create.
#
# Rules adhered to:
#   • Only standard library + pytest are used.
#   • Full, absolute paths are referenced.
#   • No output file/dir (/home/user/backups/, /home/user/backup_log.txt, etc.)
#     is tested for presence or absence here.

from pathlib import Path
import pytest

TEST_CONFIGS_DIR = Path("/home/user/test_configs")
CONFIG1_PATH = TEST_CONFIGS_DIR / "config1.ini"
CONFIG2_PATH = TEST_CONFIGS_DIR / "config2.ini"


@pytest.fixture(scope="module")
def config_dir_exists():
    """Ensure /home/user/test_configs exists and is a directory."""
    if not TEST_CONFIGS_DIR.exists():
        pytest.fail(f"Required directory {TEST_CONFIGS_DIR} is missing.")
    if not TEST_CONFIGS_DIR.is_dir():
        pytest.fail(f"{TEST_CONFIGS_DIR} exists but is not a directory.")
    return TEST_CONFIGS_DIR


def test_required_files_present(config_dir_exists):
    """Both config1.ini and config2.ini must exist."""
    missing = [p for p in (CONFIG1_PATH, CONFIG2_PATH) if not p.is_file()]
    if missing:
        pretty = ", ".join(str(p) for p in missing)
        pytest.fail(f"Missing required file(s): {pretty}")


def test_config1_contents():
    """Validate the exact contents of config1.ini."""
    expected = "[database]\nhost=localhost\nport=5432\n"
    try:
        content = CONFIG1_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file {CONFIG1_PATH} is missing.")
    # Strip trailing newlines from both to allow either 1 or 0 final NLs.
    if content.rstrip("\n") != expected.rstrip("\n"):
        pytest.fail(
            f"Contents of {CONFIG1_PATH} are not as expected.\n"
            f"Expected:\n{expected!r}\nGot:\n{content!r}"
        )


def test_config2_contents():
    """Validate the exact contents of config2.ini."""
    expected = "[web]\nhost=0.0.0.0\nport=8080\n"
    try:
        content = CONFIG2_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file {CONFIG2_PATH} is missing.")
    if content.rstrip("\n") != expected.rstrip("\n"):
        pytest.fail(
            f"Contents of {CONFIG2_PATH} are not as expected.\n"
            f"Expected:\n{expected!r}\nGot:\n{content!r}"
        )