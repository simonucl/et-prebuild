# test_initial_state.py
#
# Pytest suite to verify that the operating-system / filesystem
# is in the correct *initial* state before the student starts
# working on the “Firewall Resource-Usage Audit & Baseline Ruleset
# Proposal” exercise.
#
# Only the presence and correctness of the *input* artefact is
# validated here.  Output paths are intentionally **not** tested.

import os
import re
import pytest

SAMPLE_FILE = "/home/user/sample_firewall_output.txt"


def test_input_file_exists():
    """
    The task relies on the presence of
    /home/user/sample_firewall_output.txt.
    """
    assert os.path.isfile(
        SAMPLE_FILE
    ), f"Required input file '{SAMPLE_FILE}' is missing."


def test_sample_file_content_statistics():
    """
    Parse the sample firewall dump and verify that its statistics match
    the values expected by the downstream automated grader.  This guards
    against accidental corruption or tampering with the input file.
    """
    with open(SAMPLE_FILE, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    chain_header_re = re.compile(
        r"^Chain\s+(\S+)\s+\(policy\s+\w+\s+(\d+)\s+packets"
    )

    chains = []          # list of tuples (chain_name, packet_counter)
    explicit_rule_count = 0

    for line in lines:
        # Header lines that start with "Chain …"
        m = chain_header_re.match(line)
        if m:
            chains.append((m.group(1), int(m.group(2))))
            continue

        # Skip blank lines and table-header lines (those beginning with "pkts …")
        stripped = line.lstrip()
        if (
            not stripped  # blank
            or stripped.lower().startswith("pkts ")
        ):
            continue

        # Any remaining line that starts with a digit is an explicit rule.
        if stripped[0].isdigit():
            explicit_rule_count += 1

    # Expected values derived from the sample provided in the task description
    expected_chain_count = 3
    expected_rule_count = 5
    expected_top_chain = "INPUT"
    expected_top_chain_pkts = 104

    # ---- Assertions with helpful error messages ----
    assert (
        len(chains) == expected_chain_count
    ), f"Expected {expected_chain_count} chains, found {len(chains)}."

    assert (
        explicit_rule_count == expected_rule_count
    ), f"Expected {expected_rule_count} explicit rules, found {explicit_rule_count}."

    # Determine chain with highest packet counter
    if not chains:
        pytest.fail("No chain headers were detected in the sample file.")

    top_chain_name, top_chain_pkts = max(chains, key=lambda x: x[1])

    assert (
        top_chain_name == expected_top_chain
    ), f"Expected top chain '{expected_top_chain}', found '{top_chain_name}'."

    assert (
        top_chain_pkts == expected_top_chain_pkts
    ), f"Expected top chain to have {expected_top_chain_pkts} packets, found {top_chain_pkts}."