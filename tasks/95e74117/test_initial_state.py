# test_initial_state.py
#
# Pytest suite that validates the filesystem **before** the student
# performs any actions for the “Audit & Correct YAML/TOML Configuration”
# task.  We check only for the existence and exact contents of the two
# original configuration files.  We deliberately do NOT look for backup
# files, audit directories, or log files because those constitute output
# from the yet-to-be-executed student solution.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
CFG_YAML = HOME / "compliance/service_a/config.yaml"
CFG_TOML = HOME / "compliance/service_b/settings.toml"


@pytest.fixture(scope="module")
def expected_contents():
    """
    Returns a dictionary mapping full file paths to their required
    pre-task contents (including trailing newlines).
    """
    yaml_content = (
        "apiVersion: v1\n"
        "service:\n"
        "  enabled: false\n"
        "  port: 8080\n"
        "logging:\n"
        "  level: INFO\n"
    )

    toml_content = (
        "[server]\n"
        "active = false\n"
        "listen_ip = \"0.0.0.0\"\n"
        "listen_port = 9000\n"
        "\n"
        "[security]\n"
        "ciphers = [\"TLS_AES_128_GCM_SHA256\"]\n"
    )

    return {
        CFG_YAML: yaml_content,
        CFG_TOML: toml_content,
    }


@pytest.mark.parametrize(
    "file_path",
    [CFG_YAML, CFG_TOML],
)
def test_file_exists(file_path, expected_contents):
    """
    Ensure each required configuration file is present at the exact
    absolute path.
    """
    assert file_path.is_file(), (
        f"Expected file {file_path} to exist before the task begins, "
        "but it was not found."
    )


@pytest.mark.parametrize(
    "file_path",
    [CFG_YAML, CFG_TOML],
)
def test_file_contents_exact(file_path, expected_contents):
    """
    Validate that each configuration file contains the precise,
    byte-for-byte content expected before any modifications.
    """
    actual = file_path.read_text(encoding="utf-8")
    expected = expected_contents[file_path]
    assert (
        actual == expected
    ), (
        f"Content mismatch in {file_path}.\n\n"
        f"--- Expected (pre-task) ---\n{expected!r}\n"
        f"---   Actual on disk   ---\n{actual!r}\n"
        "The file should be in its original state before the student "
        "makes any changes."
    )