# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student’s solution runs.  It asserts that:
#   1. The configuration INI file exists and has the exact,
#      expected contents (including the final newline).
#   2. The manifests directory contains *no* “*-deployment.yaml”
#      files (it may not even exist yet).
#   3. The audit log file does *not* exist yet.
#
# Any deviation from these expectations will cause a clear,
# actionable test failure.
#
# Only stdlib + pytest are used, as required.

from pathlib import Path
import pytest

# Constants for the required filesystem layout
HOME = Path("/home/user")
KUBE_DIR = HOME / "kube-operator"
CONFIG_DIR = KUBE_DIR / "config"
MANIFESTS_DIR = KUBE_DIR / "manifests"
OUTPUT_DIR = KUBE_DIR / "output"

CONFIG_PATH = CONFIG_DIR / "app.ini"
OUTPUT_LOG_PATH = OUTPUT_DIR / "generation.log"


EXPECTED_INI_CONTENT = (
    "[staging]\n"
    "app_name=my-web\n"
    "image=example/my-web:v1.2.3\n"
    "replicas=2\n"
    "port=8080\n"
    "\n"
    "[production]\n"
    "app_name=my-web\n"
    "image=example/my-web:v1.2.3\n"
    "replicas=5\n"
    "port=80\n"
)

@pytest.mark.describe("Initial filesystem state")
class TestInitialState:
    def test_config_ini_exists_with_exact_content(self):
        """
        The configuration file must exist and match the expected
        byte-for-byte content, including the terminating newline.
        """
        assert CONFIG_PATH.is_file(), (
            f"Missing configuration file: {CONFIG_PATH}. "
            "It must be present before any processing occurs."
        )

        actual = CONFIG_PATH.read_text(encoding="utf-8")
        assert actual == EXPECTED_INI_CONTENT, (
            "The contents of {path} do not match the expected template.\n"
            "Expected:\n"
            "----\n"
            f"{EXPECTED_INI_CONTENT}"
            "----\n"
            "Got:\n"
            "----\n"
            f"{actual}"
            "----".format(path=CONFIG_PATH)
        )

    def test_no_manifests_exist_yet(self):
        """
        No *-deployment.yaml files should exist before the student code runs.
        The manifests/ directory itself may or may not exist, but if it does,
        it must not contain any generated deployment manifests.
        """
        if MANIFESTS_DIR.exists():
            assert MANIFESTS_DIR.is_dir(), (
                f"{MANIFESTS_DIR} exists but is not a directory."
            )
            deployment_files = list(MANIFESTS_DIR.glob("*-deployment.yaml"))
            assert not deployment_files, (
                "Found pre-existing deployment manifest(s):\n  "
                + "\n  ".join(str(p) for p in deployment_files)
                + "\nThe directory should be empty (or absent) before generation."
            )

    def test_generation_log_does_not_exist(self):
        """
        The audit log must not exist before generation.
        """
        assert not OUTPUT_LOG_PATH.exists(), (
            f"{OUTPUT_LOG_PATH} already exists, but it should only be created "
            "after the manifests are generated."
        )