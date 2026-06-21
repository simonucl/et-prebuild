# test_initial_state.py
#
# This pytest suite validates the OS / filesystem *before* the student
# executes their single-command solution.  It confirms that the reference
# input file exists and that, according to its current contents, the
# container with the highest CPU utilisation is “pg_db”.
#
# Do NOT modify these tests; they guarantee that the automatic grader’s
# expectations and the supplied data stay in lock-step.

import pathlib
import re

import pytest

# Absolute path to the input file provided to the student.
STATS_LOG = pathlib.Path("/home/user/run/docker_stats_sample.log")


def _parse_cpu_value(raw: str) -> float:
    """
    Convert a CPU percentage string like '72.10%' to a float (72.10).

    Raises ValueError if the format is unexpected.
    """
    if not raw.endswith("%"):
        raise ValueError(f"CPU column value {raw!r} does not end with '%'")
    # Strip the percent sign and any stray whitespace, then convert to float.
    return float(raw.rstrip("%").strip())


@pytest.mark.dependency(name="file_exists")
def test_stats_file_exists():
    """The docker_stats_sample.log file must exist before the exercise starts."""
    assert STATS_LOG.is_file(), (
        f"Required sample file not found: {STATS_LOG}. "
        "Ensure the file is present so students can parse it."
    )


@pytest.mark.dependency(depends=["file_exists"], name="header_valid")
def test_stats_header_is_present_and_well_formed():
    """
    The first line of the stats log must contain the expected header columns.
    We check for the key substrings so that minor spacing differences do not
    cause a false negative.
    """
    header = STATS_LOG.read_text().splitlines()[0]
    expected_fragments = ["CONTAINER ID", "NAME", "CPU %"]
    missing = [frag for frag in expected_fragments if frag not in header]
    assert not missing, (
        "The header of docker_stats_sample.log is missing expected column "
        f"names: {', '.join(missing)}"
    )


@pytest.mark.dependency(depends=["header_valid"])
def test_highest_cpu_container_is_pg_db():
    """
    Validate that, according to the provided stats snapshot, the container
    with the highest CPU usage is 'pg_db'.  This ensures the grading logic
    remains deterministic.
    """
    lines = STATS_LOG.read_text().splitlines()

    # Skip the header and ignore completely empty lines.
    data_lines = [ln for ln in lines[1:] if ln.strip()]
    assert data_lines, "docker_stats_sample.log contains no data lines."

    top_container = None
    top_cpu = -1.0

    whitespace_re = re.compile(r"\s+")

    for line in data_lines:
        # Collapse multiple spaces to a single separator, then split.
        columns = whitespace_re.split(line.strip())
        if len(columns) < 3:
            pytest.fail(
                "Encountered a malformed data line in docker_stats_sample.log:\n"
                f"{line!r}"
            )

        name = columns[1]           # second column
        cpu_raw = columns[2]        # third column
        try:
            cpu_val = _parse_cpu_value(cpu_raw)
        except ValueError as exc:
            pytest.fail(str(exc))

        if cpu_val > top_cpu:
            top_cpu = cpu_val
            top_container = name

    assert top_container == "pg_db", (
        f"Expected the container with highest CPU to be 'pg_db', "
        f"but found '{top_container}' (CPU={top_cpu}%)."
    )