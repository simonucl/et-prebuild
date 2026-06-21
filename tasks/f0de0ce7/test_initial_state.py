# test_initial_state.py
#
# Pytest suite that validates the starting filesystem state before the
# student performs any actions for the “IoT firmware bundle” task.
#
# Rules verified:
#   1. /home/user/firmware/configs/device.conf must exist and contain exactly
#      one line with the original hard-coded API key
#         API_KEY="DEADBEEFDEADBEEFDEADBEEFDEADBEEF"
#      terminated by a single newline.
#   2. /home/user/firmware/firewall/rules.conf must exist and contain exactly
#      three lines (each ending with '\n'):
#         ALLOW 22
#         ALLOW 8080
#         ALLOW 1883
#   3. /home/user/security_audit.log must *not* exist yet.
#
# Only stdlib and pytest are used.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
FIRMWARE_DIR = HOME / "firmware"
CONFIGS_DIR = FIRMWARE_DIR / "configs"
FIREWALL_DIR = FIRMWARE_DIR / "firewall"

DEVICE_CONF = CONFIGS_DIR / "device.conf"
FIREWALL_RULES_CONF = FIREWALL_DIR / "rules.conf"
AUDIT_LOG = HOME / "security_audit.log"

OLD_KEY = "DEADBEEFDEADBEEFDEADBEEFDEADBEEF"
EXPECTED_DEVICE_CONF_LINE = f'API_KEY="{OLD_KEY}"\n'

EXPECTED_FIREWALL_LINES = [
    "ALLOW 22\n",
    "ALLOW 8080\n",
    "ALLOW 1883\n",
]


@pytest.mark.describe("Initial filesystem state validation")
class TestInitialState:
    # ---------------------------------------------------------------------
    # Generic path existence sanity checks
    # ---------------------------------------------------------------------

    @pytest.mark.it("Firmware directory tree exists")
    def test_firmware_directories_exist(self):
        for path in (FIRMWARE_DIR, CONFIGS_DIR, FIREWALL_DIR):
            assert path.is_dir(), f"Required directory missing: {path}"

    # ---------------------------------------------------------------------
    # device.conf checks
    # ---------------------------------------------------------------------

    @pytest.mark.it("/home/user/firmware/configs/device.conf exists")
    def test_device_conf_exists(self):
        assert DEVICE_CONF.is_file(), f"Missing file: {DEVICE_CONF}"

    @pytest.mark.it("device.conf contains exactly the original hard-coded API key line")
    def test_device_conf_content(self):
        content = DEVICE_CONF.read_text(encoding="utf-8")
        assert (
            content == EXPECTED_DEVICE_CONF_LINE
        ), (
            "device.conf should contain exactly one line:\n"
            f"{EXPECTED_DEVICE_CONF_LINE!r}\n"
            f"Found:\n{content!r}"
        )

    # ---------------------------------------------------------------------
    # firewall/rules.conf checks
    # ---------------------------------------------------------------------

    @pytest.mark.it("/home/user/firmware/firewall/rules.conf exists")
    def test_firewall_rules_exists(self):
        assert FIREWALL_RULES_CONF.is_file(), f"Missing file: {FIREWALL_RULES_CONF}"

    @pytest.mark.it("firewall/rules.conf contains the expected three ALLOW lines")
    def test_firewall_rules_content(self):
        lines = FIREWALL_RULES_CONF.read_text(encoding="utf-8").splitlines(keepends=True)
        assert (
            lines == EXPECTED_FIREWALL_LINES
        ), (
            f"firewall/rules.conf should contain exactly these three lines:\n"
            f"{EXPECTED_FIREWALL_LINES!r}\n"
            f"Found:\n{lines!r}"
        )

    # ---------------------------------------------------------------------
    # security_audit.log absence check
    # ---------------------------------------------------------------------

    @pytest.mark.it("/home/user/security_audit.log must NOT exist yet")
    def test_audit_log_absent(self):
        assert (
            not AUDIT_LOG.exists()
        ), (
            f"{AUDIT_LOG} should not exist before the student starts. "
            "Please remove it so the task begins from a clean state."
        )