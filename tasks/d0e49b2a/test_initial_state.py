# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student’s deployment-promotion script is executed.
#
# It checks that the directory /home/user/deployment_configs/ exists,
# contains exactly the four expected “*.conf” files, and that the
# contents of those files match the specification given in the task
# description.  Nothing else is inspected—especially none of the
# artefacts that the student is expected to create later.

import pathlib
import textwrap
import pytest


DEPLOY_DIR = pathlib.Path("/home/user/deployment_configs/")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def read_conf_lines(path: pathlib.Path):
    """
    Return the file’s logical lines *without* trailing newlines.
    We purposefully keep leading/trailing spaces inside the lines
    because the format must match exactly.
    """
    with path.open("r", encoding="utf-8") as f:
        return [ln.rstrip("\n") for ln in f.readlines()]


# Expected (“golden”) state for each configuration file.
EXPECTED_CONFIGS = {
    "service_alpha.conf": textwrap.dedent(
        """\
        ServiceName: AlphaAPI
        Version: 1.3.7
        Environment: staging
        Status: READY"""
    ).splitlines(),
    "service_beta.conf": textwrap.dedent(
        """\
        ServiceName: BetaWorker
        Version: 3.2.4
        Environment: production
        Status: LIVE"""
    ).splitlines(),
    "service_gamma.conf": textwrap.dedent(
        """\
        ServiceName: GammaDB
        Version: 0.9.12
        Environment: staging
        Status: READY"""
    ).splitlines(),
    "service_delta.conf": textwrap.dedent(
        """\
        ServiceName: DeltaUI
        Version: 2.1.0
        Environment: staging
        Status: IN_TEST"""
    ).splitlines(),
}

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_deploy_directory_exists():
    assert DEPLOY_DIR.is_dir(), (
        f"Expected directory {DEPLOY_DIR} to exist, "
        "but it is missing."
    )


def test_exact_conf_file_set():
    """
    The directory must contain *exactly* the four expected .conf files
    and no others.  This protects against both missing and extraneous
    configs.
    """
    conf_files = {p.name for p in DEPLOY_DIR.glob("*.conf")}
    expected_files = set(EXPECTED_CONFIGS)
    missing = expected_files - conf_files
    extra = conf_files - expected_files

    message_lines = []
    if missing:
        message_lines.append(
            f"Missing config file(s): {', '.join(sorted(missing))}"
        )
    if extra:
        message_lines.append(
            f"Unexpected additional .conf file(s): "
            f"{', '.join(sorted(extra))}"
        )

    assert not missing and not extra, "\n".join(message_lines) or (
        "Config files do not match the expected set."
    )


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_CONFIGS.items())
def test_conf_file_contents(filename, expected_lines):
    """
    Validate the exact, line-for-line contents of each configuration file.
    """
    path = DEPLOY_DIR / filename
    assert path.is_file(), f"Expected file {path} to exist."

    actual_lines = read_conf_lines(path)

    # Fast fail on line-count mismatch for a clearer message
    assert len(actual_lines) == len(expected_lines), (
        f"{filename} should have {len(expected_lines)} lines but has "
        f"{len(actual_lines)}."
    )

    for idx, (exp, act) in enumerate(zip(expected_lines, actual_lines), start=1):
        assert act == exp, (
            f"{filename}, line {idx} differs:\n"
            f"EXPECTED: '{exp}'\n"
            f"ACTUAL  : '{act}'"
        )