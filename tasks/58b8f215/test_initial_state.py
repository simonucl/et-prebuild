# test_initial_state.py
"""
Pytest suite that verifies the initial, pristine filesystem state **before**
the student performs any task.  These tests assert that all required template
files and directories exist with the exact expected contents, and that no
output artefacts have been pre-generated.

The checks performed:
1. Mandatory directories exist and are directories.
2. Mandatory source files exist with *byte-exact* contents (including the
   trailing newline).
3. The writable “generated” directory exists but does **not** yet contain
   any of the files the student is supposed to create.
"""

import pathlib
import pytest


HOME = pathlib.Path("/home/user")
QA_ENVS = HOME / "qa_envs"

BASE_DIR = QA_ENVS / "base"
OVERRIDES_DIR = QA_ENVS / "overrides"
GENERATED_DIR = QA_ENVS / "generated"

# ---------- Expected file contents (byte-exact, incl. trailing newline) ----------

EXPECTED_APP_CONFIG = (
    "app:\n"
    "  name: DemoApp\n"
    "  version: \"1.0.0\"\n"
    "  debug: false\n"
    "database:\n"
    "  host: localhost\n"
    "  port: 5432\n"
    "  username: demo\n"
    "  password: demo123\n"
)

EXPECTED_DEV_OVERRIDE = (
    "app:\n"
    "  version: \"1.1.0\"\n"
    "  debug: true\n"
    "database:\n"
    "  host: dev-db.internal\n"
    "  port: 5433\n"
    "  username: dev_user\n"
    "  password: dev_pass\n"
    "features:\n"
    "  experimental: true\n"
    "  logging: verbose\n"
)

EXPECTED_TEST_OVERRIDE = (
    "app:\n"
    "  version: \"1.1.0\"\n"
    "database:\n"
    "  host: test-db.internal\n"
    "  port: 5434\n"
    "  username: test_user\n"
    "  password: test_pass\n"
    "features:\n"
    "  experimental: false\n"
    "  logging: normal\n"
)

EXPECTED_SETTINGS_TOML = (
    "[build]\n"
    "threads = 8\n"
    "optimize = true\n"
    "\n"
    "[qa]\n"
    "environment = \"multi\"\n"
)

# -------------------------------------------------------------------------------


# ------------------------------- Helper utils ----------------------------------

def assert_file_content(path: pathlib.Path, expected: str) -> None:
    """
    Assert that `path` exists, is a file, and its bytes match `expected`
    exactly.  A helpful error message is produced if any check fails.
    """
    assert path.exists(), f"Expected file '{path}' is missing."
    assert path.is_file(), f"Path '{path}' exists but is not a file."
    actual = path.read_text(encoding="utf-8")
    assert actual == expected, (
        f"Contents of '{path}' differ from the expected template.\n"
        "----- Expected -----\n"
        f"{expected!r}\n"
        "------ Actual ------\n"
        f"{actual!r}\n"
    )

# --------------------------------- The tests -----------------------------------

def test_directories_exist_and_have_correct_type():
    """The three core directories must exist and be directories."""
    for directory in (BASE_DIR, OVERRIDES_DIR, GENERATED_DIR):
        assert directory.exists(), f"Required directory '{directory}' is missing."
        assert directory.is_dir(), f"Path '{directory}' exists but is not a directory."


def test_base_app_config_file():
    """The immutable golden app_config.yml must exist with exact contents."""
    path = BASE_DIR / "app_config.yml"
    assert_file_content(path, EXPECTED_APP_CONFIG)


def test_dev_override_file():
    """The dev override YAML must exist with exact contents."""
    path = OVERRIDES_DIR / "dev.yml"
    assert_file_content(path, EXPECTED_DEV_OVERRIDE)


def test_test_override_file():
    """The test override YAML must exist with exact contents."""
    path = OVERRIDES_DIR / "test.yml"
    assert_file_content(path, EXPECTED_TEST_OVERRIDE)


def test_settings_toml_initial_state():
    """settings.toml must exist and have the unmodified 'multi' environment."""
    path = QA_ENVS / "settings.toml"
    assert_file_content(path, EXPECTED_SETTINGS_TOML)


def test_generated_directory_initially_empty():
    """
    The student should start with an empty 'generated' directory—specifically,
    none of the files they are expected to create should already be present.
    """
    forbidden = {
        GENERATED_DIR / "dev_full.yml",
        GENERATED_DIR / "test_full.yml",
        GENERATED_DIR / "verification.log",
    }
    for fpath in forbidden:
        assert not fpath.exists(), (
            f"File '{fpath}' should NOT exist yet; the student must create it as "
            "part of the assignment."
        )