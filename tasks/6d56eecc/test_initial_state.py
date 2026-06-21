# test_initial_state.py
#
# Pytest suite that validates the **initial** (pre-task) filesystem state
# for the “firewall rules” challenge.
#
# Rules verified:
# 1. Directory /home/user/firewall/ exists.
# 2. File /home/user/firewall/current_rules.list exists and contains
#    exactly the three expected lines (in order, with trailing newlines).
# 3. Files that the student is supposed to create **later** do *not* exist:
#    - /home/user/firewall/updated_rules.list
#    - /home/user/firewall/update_report.log
#
# Any deviation from these expectations will cause a clear, descriptive
# test failure.

import os
import pytest

FIREWALL_DIR = "/home/user/firewall"
CURRENT_RULES = os.path.join(FIREWALL_DIR, "current_rules.list")
UPDATED_RULES = os.path.join(FIREWALL_DIR, "updated_rules.list")
UPDATE_REPORT = os.path.join(FIREWALL_DIR, "update_report.log")

EXPECTED_LINES = [
    "-A INPUT -p tcp --dport 22 -j ACCEPT\n",
    "-A INPUT -p icmp -j ACCEPT\n",
    "-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT\n",
]


def test_firewall_directory_exists():
    assert os.path.isdir(
        FIREWALL_DIR
    ), f"Required directory {FIREWALL_DIR!r} is missing."


def test_current_rules_file_exists():
    assert os.path.isfile(
        CURRENT_RULES
    ), f"Required file {CURRENT_RULES!r} does not exist."


def test_current_rules_file_contents_exact():
    with open(CURRENT_RULES, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert (
        lines == EXPECTED_LINES
    ), (
        f"{CURRENT_RULES!r} must contain exactly three specific lines.\n"
        f"Expected:\n{''.join(EXPECTED_LINES)}\n"
        f"Found:\n{''.join(lines)}"
    )


@pytest.mark.parametrize(
    "path",
    [UPDATED_RULES, UPDATE_REPORT],
)
def test_future_output_files_do_not_exist_yet(path):
    assert not os.path.exists(
        path
    ), f"File {path!r} should not exist before the student runs their commands."