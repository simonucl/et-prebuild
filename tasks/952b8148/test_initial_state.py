# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating
# system / filesystem before the student performs any actions for the
# “capacity-planner” exercise.
#
# Assumptions (truth values):
#   • Two configuration files already exist and contain the *original*
#    , un-modified data.
#   • The log file that the student must create does **not** exist yet.
#
# What we check:
#   1. /home/user/projects/capplan exists and is a directory.
#   2. /home/user/projects/capplan/resources.yaml
#        – exists, is readable, is valid YAML for the limited subset we
#          need (parsed with a tiny custom parser—no external deps).
#        – contains exactly **two** server maps: db01 and web01 with
#          the expected cpu / memory integers.
#        – MUST NOT contain cache01 (that is the student’s addition).
#   3. /home/user/projects/capplan/thresholds.toml
#        – exists, is readable, parsable with a minimalist TOML reader.
#        – cpu.warning == 70, cpu.critical == 90
#          memory.warning == 75, memory.critical == 95
#   4. /home/user/projects/capplan/planner.log does **not** exist yet.
#
# If any assertion fails the accompanying message should make it clear
# what is wrong so the learner can diagnose quickly.
#
# Only stdlib + pytest are used.

import os
import re
from pathlib import Path

CAPPLAN_DIR = Path("/home/user/projects/capplan")
RESOURCES_YAML = CAPPLAN_DIR / "resources.yaml"
THRESHOLDS_TOML = CAPPLAN_DIR / "thresholds.toml"
PLANNER_LOG = CAPPLAN_DIR / "planner.log"


def parse_resources_yaml(path: Path):
    """
    Very small YAML subset parser sufficient for:

    servers:
      - name: db01
        cpu: 4
        memory: 16
      - name: web01
        cpu: 2
        memory: 8

    Returns
    -------
    list of dict
        Each dict -> {"name": str, "cpu": int, "memory": int}
    """
    servers = []
    current = None
    with path.open(encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.strip() == "servers:":
                # start of list; continue
                continue
            # Match   - name: something
            m_name = re.match(r"\s*-\s+name:\s+(\S+)", line)
            if m_name:
                # push previous if any
                if current:
                    servers.append(current)
                current = {"name": m_name.group(1)}
                continue
            # Match attribute lines (cpu & memory)
            m_attr = re.match(r"\s*(cpu|memory):\s+(\d+)", line)
            if m_attr and current is not None:
                key, value = m_attr.group(1), int(m_attr.group(2))
                current[key] = value
    # Append last record
    if current:
        servers.append(current)
    return servers


def parse_thresholds_toml(path: Path):
    """
    Minimal reader for the specific TOML format used here.

    Returns
    -------
    dict
        {
            "cpu": {"warning": int, "critical": int},
            "memory": {"warning": int, "critical": int}
        }
    """
    result = {}
    section = None
    with path.open(encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            # Section header e.g. [cpu]
            m_sec = re.match(r"\[(\w+)]", line)
            if m_sec:
                section = m_sec.group(1)
                result[section] = {}
                continue
            # Key/value pair  key = value
            if "=" in line and section:
                key_part, value_part = line.split("=", 1)
                key = key_part.strip()
                value = value_part.strip()
                # Accept only integers for this exercise
                try:
                    value_int = int(value)
                except ValueError as exc:
                    raise ValueError(
                        f"Non-integer value in {section}.{key}: {value}"
                    ) from exc
                result[section][key] = value_int
    return result


def test_capplan_directory_exists():
    assert CAPPLAN_DIR.is_dir(), (
        f"Expected directory {CAPPLAN_DIR} to exist but it was not found."
    )


def test_resources_yaml_initial_content():
    assert RESOURCES_YAML.is_file(), (
        f"{RESOURCES_YAML} is missing. The exercise starts with this file present."
    )

    servers = parse_resources_yaml(RESOURCES_YAML)

    # Expect exactly two servers before student adds the 3rd.
    expected = [
        {"name": "db01", "cpu": 4, "memory": 16},
        {"name": "web01", "cpu": 2, "memory": 8},
    ]
    assert servers == expected, (
        "resources.yaml should initially contain ONLY the following two "
        f"servers:\n{expected}\n\nCurrent parsed content:\n{servers}\n\n"
        "Make sure the starting repository has not already been modified."
    )


def test_thresholds_toml_initial_content():
    assert THRESHOLDS_TOML.is_file(), (
        f"{THRESHOLDS_TOML} is missing. The exercise starts with this file present."
    )

    data = parse_thresholds_toml(THRESHOLDS_TOML)

    expected = {
        "cpu": {"warning": 70, "critical": 90},
        "memory": {"warning": 75, "critical": 95},
    }
    assert data == expected, (
        "thresholds.toml should start with the following numeric values:\n"
        f"{expected}\n\nCurrent parsed content:\n{data}\n\n"
        "If these numbers differ, the initial repository state is wrong."
    )


def test_planner_log_absent():
    assert not PLANNER_LOG.exists(), (
        f"{PLANNER_LOG} already exists, but this log file is supposed to be "
        "created by the student. Please remove it from the starter repository."
    )