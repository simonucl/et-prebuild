# test_initial_state.py
#
# PyTest suite that validates the **initial** (i.e. expected-final) state of
# the local developer scaffold for the cloud-migration exercise.
#
# The checks purposefully fail when anything is missing, malformed or has the
# wrong permissions so that a student knows exactly what still needs to be
# created/adjusted.

import os
import re
from pathlib import Path

import pytest

ROOT = Path("/home/user/cloud-migration")

# --------------------------------------------------------------------------- #
# Expected directory layout (absolute paths)                                  #
# --------------------------------------------------------------------------- #
EXPECTED_DIRS = {
    ROOT,
    ROOT / "configs",
    ROOT / "scripts",
    ROOT / "logs",
}

# --------------------------------------------------------------------------- #
# Expected files and their **exact** contents                                 #
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    ROOT / "configs" / "dev-context.yaml": (
        "apiVersion: v1\n"
        "kind: Config\n"
        "clusters:\n"
        "- cluster:\n"
        "    server: https://dev.k8s.local\n"
        "  name: dev-cluster\n"
        "contexts:\n"
        "- context:\n"
        "    cluster: dev-cluster\n"
        "    user: dev-user\n"
        "  name: dev-context\n"
        "current-context: dev-context\n"
        "users:\n"
        "- name: dev-user\n"
        "  user:\n"
        "    token: DEV123TOKEN\n"
    ),
    ROOT / "scripts" / "set-dev-env.sh": (
        "#!/usr/bin/env bash\n"
        "export K8S_CLUSTER_NAME=dev-cluster\n"
        "export K8S_NAMESPACE=default\n"
        "export IMAGE_TAG=v1.0.0\n"
    ),
    ROOT / "Dockerfile": (
        "FROM alpine:3.17\n"
        "RUN apk add --no-cache python3 py3-pip\n"
        "COPY . /app\n"
        "WORKDIR /app\n"
        "CMD [\"python3\", \"-m\", \"http.server\", \"8080\"]\n"
    ),
    ROOT / "README.md": (
        "# Cloud Migration Dev Environment\n"
        "This repository provides the minimal scaffolding required to reproduce our\n"
        "development Kubernetes context locally. It includes:\n"
        "* kubectl context for the `dev-cluster`\n"
        "* helper script for environment variables\n"
        "* lightweight Alpine-based Dockerfile for service prototyping\n"
    ),
    ROOT / "logs" / "setup.log": None,  # contents are validated separately
}

LOG_PATH = ROOT / "logs" / "setup.log"
LOG_LINE_REGEX = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} \| .+$"
)

# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def read_file_bytes(path: Path) -> bytes:
    with path.open("rb") as fp:
        return fp.read()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_directories_exist_and_no_extras():
    """
    1. All required directories exist.
    2. No *extra* files/directories are present anywhere under ROOT.
       (Every entry must belong to EXPECTED_DIRS or EXPECTED_FILES.)
    """
    # --- 1. Required directories ---
    missing = [d for d in EXPECTED_DIRS if not d.is_dir()]
    assert not missing, (
        "The following required directories are missing:\n"
        + "\n".join(str(d) for d in missing)
    )

    # --- 2. No extras ---
    allowed_paths = set(EXPECTED_DIRS) | set(EXPECTED_FILES)
    extras = []
    for path, _, files in os.walk(ROOT):
        p = Path(path)
        # directory itself
        if p not in allowed_paths:
            extras.append(p)
        # contained files
        for f in files:
            fp = p / f
            if fp not in allowed_paths:
                extras.append(fp)

    assert not extras, (
        "Unexpected files/directories found under /home/user/cloud-migration:\n"
        + "\n".join(str(e) for e in sorted(extras))
    )


@pytest.mark.parametrize("file_path", [*EXPECTED_FILES])
def test_required_files_exist(file_path: Path):
    assert file_path.is_file(), f"Required file is missing: {file_path}"


@pytest.mark.parametrize(
    ("file_path", "expected_content"),
    [(p, c) for p, c in EXPECTED_FILES.items() if c is not None],
)
def test_file_contents_exact_match(file_path: Path, expected_content: str):
    actual_bytes = read_file_bytes(file_path)
    expected_bytes = expected_content.encode()

    assert (
        actual_bytes == expected_bytes
    ), f"Contents of {file_path} do not match the specification exactly."


def test_set_dev_env_script_is_executable():
    script = ROOT / "scripts" / "set-dev-env.sh"
    mode = script.stat().st_mode
    assert (
        mode & 0o100
    ), f"Script {script} is not executable by the current user (missing +x)."


def test_setup_log_format_and_length():
    assert LOG_PATH.is_file(), f"Log file does not exist: {LOG_PATH}"

    lines = LOG_PATH.read_text().splitlines()
    assert len(lines) >= 5, (
        f"Log file {LOG_PATH} must contain at least 5 lines. "
        f"Currently has {len(lines)}."
    )

    bad_lines = [
        (i + 1, line) for i, line in enumerate(lines) if not LOG_LINE_REGEX.match(line)
    ]
    assert not bad_lines, (
        f"The following lines in {LOG_PATH} do not match the required pattern "
        f"YYYY-MM-DD HH:MM:SS | <command>:\n"
        + "\n".join(f"Line {ln}: {txt}" for ln, txt in bad_lines)
    )