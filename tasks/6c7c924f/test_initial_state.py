# test_initial_state.py
#
# This pytest file validates that the starting filesystem state is exactly
# what the exercise description promises *before* the student performs any
# action.  If any of these tests fail, the exercise itself is invalid and
# the learner will be blocked for reasons outside of their control.
#
# NOTE:
#   - We intentionally do NOT check for the presence of the file
#     /home/user/deploy/release-1.2.4.log, because that file is supposed to
#     be created by the learner.  The rubric explicitly forbids testing for
#     any output artifacts up-front.

import os
import re
import sys
import pathlib
import pytest

# tomllib is in the stdlib from Python 3.11 onward.  For 3.10 we can fall
# back to the external "tomli" package **if** it happens to be available in
# the execution environment, but we do not add it as a hard dependency.
try:
    import tomllib  # Python ≥3.11
except ModuleNotFoundError:  # pragma: no cover
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover
        tomllib = None  # type: ignore


DEPLOY_DIR = pathlib.Path("/home/user/deploy")
CONFIG_YAML = DEPLOY_DIR / "config.yaml"
METADATA_TOML = DEPLOY_DIR / "metadata.toml"


@pytest.mark.parametrize(
    "path",
    [DEPLOY_DIR, CONFIG_YAML, METADATA_TOML],
)
def test_paths_exist(path):
    """Validate that required starting paths actually exist."""
    assert path.exists(), f"Expected {path} to exist, but it does not."


def _parse_yaml_like(lines):
    """
    A _very_ small YAML helper that only understands the specific subset we
    need for this exercise: 'key: "value"' pairs at the top level.

    Returns
    -------
    dict[str, str]
        Mapping of key → value found in the YAML snippet.
    """
    kv_pattern = re.compile(r'^([a-zA-Z0-9_]+):\s*["\']?([^"\']+)["\']?\s*$')
    result = {}
    for ln in lines:
        m = kv_pattern.match(ln.rstrip())
        if m:
            key, value = m.groups()
            result[key] = value
    return result


def test_config_yaml_initial_state():
    """
    Ensure /home/user/deploy/config.yaml is in the pristine 1.2.3 state and
    does NOT yet contain a release_date key.
    """
    with CONFIG_YAML.open("rt", encoding="utf-8") as fh:
        contents = fh.readlines()

    data = _parse_yaml_like(contents)

    # Basic sanity keys
    assert data.get("app_name") == "WeatherApp", (
        "config.yaml should have app_name: 'WeatherApp' in the initial state."
    )
    assert data.get("version") == "1.2.3", (
        "config.yaml must start with version '1.2.3' so the learner can bump it."
    )
    assert data.get("environment") == "staging", (
        "config.yaml should have environment: 'staging' as per the spec."
    )

    # release_date must NOT be present yet
    assert "release_date" not in data, (
        "config.yaml already contains a release_date key; "
        "the learner should be responsible for adding it."
    )


@pytest.mark.skipif(
    tomllib is None,
    reason="tomllib/tomli is not available in this Python version",
)
def test_metadata_toml_initial_state():
    """
    Validate that /home/user/deploy/metadata.toml is exactly in the expected
    pre-task state.
    """
    with METADATA_TOML.open("rb") as fh:
        data = tomllib.load(fh)

    # -------- [package] table validation -----------
    pkg = data.get("package")
    assert pkg is not None, "metadata.toml is missing the required [package] table."

    assert pkg.get("name") == "weather_app", (
        "metadata.toml [package] table should contain name = 'weather_app'."
    )
    assert pkg.get("version") == "1.2.3", (
        "metadata.toml should start with version = '1.2.3' so it can be bumped."
    )

    # release_date must NOT be present yet
    assert "release_date" not in pkg, (
        "[package] already has a release_date key; that should be added by the learner."
    )

    # -------- [build] table sanity check ----------
    build = data.get("build")
    assert build is not None, "metadata.toml is missing the required [build] table."
    assert build.get("target") == "x86_64", (
        "metadata.toml [build] table should contain target = 'x86_64'."
    )