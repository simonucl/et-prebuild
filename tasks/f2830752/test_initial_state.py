# test_initial_state.py
"""
Pytest suite that validates the **initial** filesystem state before the
student performs any hardening actions.

Checks performed:
1. /home/user/configs exists and is writable.
2. /home/user/configs/ssh_app.yml exists with the original (insecure) content.
3. /home/user/configs/etcd_service.toml exists with the original content.
4. /home/user/configs/hardening.log must NOT yet exist.

If any assertion fails, the accompanying message tells exactly what is wrong.
"""
import os
import pytest

CONFIG_DIR = "/home/user/configs"
SSH_YAML = os.path.join(CONFIG_DIR, "ssh_app.yml")
ETCD_TOML = os.path.join(CONFIG_DIR, "etcd_service.toml")
HARDEN_LOG = os.path.join(CONFIG_DIR, "hardening.log")


@pytest.fixture(scope="module")
def ssh_expected():
    """
    Return the exact bytes (as str) expected for the initial ssh_app.yml file,
    including the single trailing newline.
    """
    return (
        "port: 22\n"
        "permit_root_login: yes\n"
        "password_authentication: yes\n"
        "max_auth_tries: 6\n"
    )


@pytest.fixture(scope="module")
def etcd_expected():
    """
    Return the exact bytes (as str) expected for the initial etcd_service.toml
    file, including the single trailing newline.
    """
    return (
        "[Service]\n"
        "enable_debug = true\n"
        "quota_backend_bytes = 0\n"
        "\n"
        "[Security]\n"
        "token = \"simple\"\n"
        "client_cert_auth = false\n"
    )


def test_configs_directory_exists_and_writable():
    assert os.path.isdir(
        CONFIG_DIR
    ), f"Required directory {CONFIG_DIR!r} is missing."
    assert os.access(
        CONFIG_DIR, os.W_OK
    ), f"Directory {CONFIG_DIR!r} exists but is not writable by the current user."


def test_ssh_app_yml_initial_state(ssh_expected):
    assert os.path.isfile(
        SSH_YAML
    ), f"Initial file {SSH_YAML!r} is missing."
    with open(SSH_YAML, "r", encoding="utf-8") as fh:
        content = fh.read()

    assert (
        content == ssh_expected
    ), (
        f"{SSH_YAML!r} does not match the expected initial content.\n"
        "Expected:\n"
        f"---\n{ssh_expected}---\n"
        "Got:\n"
        f"---\n{content}---"
    )

    # Ensure exactly one trailing newline.
    assert not content.endswith("\n\n"), (
        f"{SSH_YAML!r} contains more than one trailing newline."
    )


def test_etcd_service_toml_initial_state(etcd_expected):
    assert os.path.isfile(
        ETCD_TOML
    ), f"Initial file {ETCD_TOML!r} is missing."
    with open(ETCD_TOML, "r", encoding="utf-8") as fh:
        content = fh.read()

    assert (
        content == etcd_expected
    ), (
        f"{ETCD_TOML!r} does not match the expected initial content.\n"
        "Expected:\n"
        f"---\n{etcd_expected}---\n"
        "Got:\n"
        f"---\n{content}---"
    )

    # Ensure exactly one trailing newline.
    assert not content.endswith("\n\n"), (
        f"{ETCD_TOML!r} contains more than one trailing newline."
    )


def test_hardening_log_absent():
    assert not os.path.exists(
        HARDEN_LOG
    ), (
        f"{HARDEN_LOG!r} should NOT exist yet; it will be created during "
        "the hardening process."
    )