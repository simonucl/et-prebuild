# test_initial_state.py
#
# This pytest file validates the *initial* filesystem state that must already
# exist before the student performs any actions.  It checks that the input
# release tree under /home/user/releases/2024-06-01/ is present and that the
# contents of all manifest.yaml and config.env files match the specification
# exactly.  It intentionally does *not* look at /home/user/deployment-output/
# or any other “output” location—those are the artefacts the student will
# create later.

import pathlib
import pytest

RELEASE_ROOT = pathlib.Path("/home/user/releases/2024-06-01")

# --------------------------------------------------------------------------- #
# Expected ground-truth data for each micro-service.                           #
# --------------------------------------------------------------------------- #

SERVICES = {
    "auth-service": {
        "manifest": (
            "metadata:\n"
            "  service: auth-service\n"
            "  version: \"2.1.0\"\n"
            "  container:\n"
            "    port: 7000\n"
        ),
        "config": [
            "DB_HOST=auth-db.internal",
            "DB_PORT=5432",
            "JWT_SECRET=s3cr3t",
            "LOG_LEVEL=INFO",
        ],
    },
    "billing-service": {
        "manifest": (
            "metadata:\n"
            "  service: billing-service\n"
            "  version: \"3.4.2\"\n"
            "  container:\n"
            "    port: 7100\n"
        ),
        "config": [
            "DB_HOST=billing-db.internal",
            "DB_PORT=5432",
            "PAYMENT_GATEWAY_TOKEN=abcd1234",
            "LOG_LEVEL=INFO",
            "CURRENCY=USD",
        ],
    },
    "report-service": {
        "manifest": (
            "metadata:\n"
            "  service: report-service\n"
            "  version: \"1.8.0\"\n"
            "  container:\n"
            "    port: 7200\n"
        ),
        "config": [
            "DB_HOST=report-db.internal",
            "DB_PORT=5432",
            "REPORT_CACHE_SIZE=512",
            "LOG_LEVEL=DEBUG",
        ],
    },
}

# --------------------------------------------------------------------------- #
# Helper functions                                                             #
# --------------------------------------------------------------------------- #


def read_text_file(path: pathlib.Path) -> str:
    """
    Read a UTF-8 text file and return its exact contents.
    """
    return path.read_text(encoding="utf-8")


def read_lines(path: pathlib.Path) -> list[str]:
    """
    Read a text file and return a list of its lines *without* trailing
    newline characters.
    """
    return path.read_text(encoding="utf-8").splitlines()


# --------------------------------------------------------------------------- #
# Tests                                                                        #
# --------------------------------------------------------------------------- #


def test_release_root_exists_and_is_dir():
    assert RELEASE_ROOT.exists(), f"Expected release root {RELEASE_ROOT} to exist."
    assert RELEASE_ROOT.is_dir(), f"{RELEASE_ROOT} exists but is not a directory."


@pytest.mark.parametrize("service", sorted(SERVICES))
def test_service_directory_exists(service):
    service_dir = RELEASE_ROOT / service
    assert service_dir.exists(), f"Service directory {service_dir} is missing."
    assert service_dir.is_dir(), f"{service_dir} exists but is not a directory."


@pytest.mark.parametrize("service,data", SERVICES.items())
def test_manifest_contents(service, data):
    manifest_path = RELEASE_ROOT / service / "manifest.yaml"
    assert manifest_path.exists(), f"Missing manifest.yaml at {manifest_path}"
    file_contents = read_text_file(manifest_path)

    # Allow an optional single trailing newline in the actual file.
    expected = data["manifest"].rstrip("\n")
    actual = file_contents.rstrip("\n")

    assert (
        actual == expected
    ), (
        f"manifest.yaml for {service} does not match expected content.\n\n"
        f"Expected:\n{data['manifest']!r}\n\nActual:\n{file_contents!r}"
    )


@pytest.mark.parametrize("service,data", SERVICES.items())
def test_config_env_contents(service, data):
    env_path = RELEASE_ROOT / service / "config.env"
    assert env_path.exists(), f"Missing config.env at {env_path}"
    actual_lines = read_lines(env_path)
    expected_lines = data["config"]

    assert (
        actual_lines == expected_lines
    ), (
        f"config.env for {service} does not match expected lines.\n\n"
        f"Expected ({len(expected_lines)} lines):\n{expected_lines}\n\n"
        f"Actual ({len(actual_lines)} lines):\n{actual_lines}"
    )