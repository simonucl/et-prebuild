# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem for the
# “network-diagnostic” exercise **before** the student starts writing code.
#
# It checks that:
#   1. The required /home/user/net_samples directory exists.
#   2. All three expected raw capture files are present.
#   3. ping4.txt and ping6.txt each contain a summary line with the *expected*
#      packet counts (4 transmitted, 4 received, 0 % loss).
#   4. ss.txt contains exactly 2 LISTEN, 2 ESTAB/ESTABLISHED and 1 TIME-WAIT
#      TCP rows.
#
# No assertions are made about any output directory or files — we must **not**
# look at /home/user/net_diag at this time.


import os
import re
import pytest
from collections import Counter
from typing import Tuple, Dict


NET_SAMPLES_DIR = "/home/user/net_samples"
PING4_PATH = os.path.join(NET_SAMPLES_DIR, "ping4.txt")
PING6_PATH = os.path.join(NET_SAMPLES_DIR, "ping6.txt")
SS_PATH = os.path.join(NET_SAMPLES_DIR, "ss.txt")


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
PING_RE = re.compile(
    r"""^
        \s*(\d+)           # transmitted
        \s+packets\stransmitted,\s*
        (\d+)              # received
        \s+received,\s*
        (\d+)              # loss %
        %\s+packet\s+loss   # literal
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _extract_ping_stats(text: str) -> Tuple[int, int, int]:
    """
    Parse the single summary line at the end of a ping capture and return
    (transmitted, received, loss_percent).

    Raises a ValueError if the line cannot be found / parsed.
    """
    for line in reversed(text.splitlines()):
        m = PING_RE.search(line)
        if m:
            return tuple(int(g) for g in m.groups())
    raise ValueError("No valid ping summary line found.")


def _count_tcp_states(lines: str) -> Dict[str, int]:
    """
    Return a dict with counts of LISTEN, ESTABLISHED, TIME-WAIT states
    for TCP rows only, based on `ss -tuna` capture.
    """
    counter = Counter()
    for raw in lines.splitlines():
        line = raw.strip()
        if not line:
            continue
        # Skip header rows that usually start with 'State' or 'Netid State'
        if line.startswith(("State", "Netid")):
            continue

        parts = line.split()
        if not parts:
            continue

        # Two possible formats:
        #   Netid State Recv-Q ...
        #   State  Recv-Q ...
        if parts[0] == "tcp":
            # Newer iproute2: first column is Netid, second is State
            state = parts[1]
        else:
            state = parts[0]

        if state in {"LISTEN", "ESTABLISHED", "ESTAB", "TIME-WAIT"}:
            if state == "ESTAB":  # normalise
                state = "ESTABLISHED"
            counter[state] += 1
    return counter


# --------------------------------------------------------------------------- #
#                        ***        TESTS        ***                         #
# --------------------------------------------------------------------------- #
def test_net_samples_directory_exists():
    assert os.path.isdir(
        NET_SAMPLES_DIR
    ), f"Required directory {NET_SAMPLES_DIR!r} does not exist."


@pytest.mark.parametrize(
    "path",
    [PING4_PATH, PING6_PATH, SS_PATH],
)
def test_input_files_exist(path):
    assert os.path.isfile(path), f"Required input file {path!r} is missing."


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(PING4_PATH, id="ping4.txt"),
        pytest.param(PING6_PATH, id="ping6.txt"),
    ],
)
def test_ping_summary_values(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        text = fh.read()

    transmitted, received, loss = _extract_ping_stats(text)

    assert transmitted == 4, f"{os.path.basename(path)}: expected 4 packets transmitted, found {transmitted}."
    assert received == 4, f"{os.path.basename(path)}: expected 4 packets received, found {received}."
    assert (
        loss == 0
    ), f"{os.path.basename(path)}: expected 0 % packet loss, found {loss}%."


def test_ss_tcp_state_counts():
    with open(SS_PATH, "r", encoding="utf-8", errors="ignore") as fh:
        lines = fh.read()

    counts = _count_tcp_states(lines)

    # Build informative message first:
    msg_lines = [f"Computed TCP state counts from {SS_PATH}:"]
    for k in ("LISTEN", "ESTABLISHED", "TIME-WAIT"):
        msg_lines.append(f"  {k:<12}: {counts.get(k, 0)}")
    debug_msg = "\n".join(msg_lines)

    # Now assert individual counts
    assert counts.get("LISTEN", 0) == 2, debug_msg + "\nExpected LISTEN = 2."
    assert (
        counts.get("ESTABLISHED", 0) == 2
    ), debug_msg + "\nExpected ESTABLISHED = 2."
    assert (
        counts.get("TIME-WAIT", 0) == 1
    ), debug_msg + "\nExpected TIME-WAIT = 1."