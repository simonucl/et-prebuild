# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must
# exist _before_ the student performs any action.  It checks that the three
# Deployment manifests are present at their exact absolute paths and that
# their contents match the specification byte-for-byte (including the single
# trailing newline).  No assertions are made about any output artefacts.

import os
import pathlib

import pytest

MANIFEST_DIR = pathlib.Path("/home/user/manifests")

# Expected contents for each manifest (including the single trailing newline)
EXPECTED_MANIFESTS = {
    MANIFEST_DIR / "frontend-deploy.json": """{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "frontend",
    "namespace": "prod",
    "labels": {
      "app": "frontend"
    }
  },
  "spec": {
    "replicas": 3,
    "template": {
      "metadata": {
        "labels": {
          "app": "frontend"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "frontend",
            "image": "company/frontend:v2"
          }
        ]
      }
    }
  }
}
""",
    MANIFEST_DIR / "backend-deploy.json": """{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "backend",
    "namespace": "prod",
    "labels": {
      "app": "backend"
    }
  },
  "spec": {
    "replicas": 2,
    "template": {
      "metadata": {
        "labels": {
          "app": "backend"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "backend",
            "image": "company/backend:v1"
          }
        ]
      }
    }
  }
}
""",
    MANIFEST_DIR / "worker-deploy.json": """{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "worker",
    "namespace": "batch",
    "labels": {
      "app": "worker"
    }
  },
  "spec": {
    "replicas": 4,
    "template": {
      "metadata": {
        "labels": {
          "app": "worker"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "worker",
            "image": "company/worker:v5"
          }
        ]
      }
    }
  }
}
""",
}


def test_manifest_directory_exists():
    assert MANIFEST_DIR.is_dir(), (
        f"The manifests directory is missing at {MANIFEST_DIR}. "
        "It must exist before the student starts."
    )


@pytest.mark.parametrize("path", list(EXPECTED_MANIFESTS.keys()))
def test_manifest_file_exists(path: pathlib.Path):
    assert path.is_file(), (
        f"Expected manifest file '{path}' is missing. "
        "Ensure the initial state contains exactly the three specified JSON files."
    )


@pytest.mark.parametrize("path,expected_content", EXPECTED_MANIFESTS.items())
def test_manifest_file_content_exact(path: pathlib.Path, expected_content: str):
    actual_content = path.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), (
        f"Content of '{path}' does not match the expected specification.\n"
        "If this file was modified or formatted differently, restore it to "
        "the exact state described in the task."
    )


def test_no_unexpected_files_in_manifest_dir():
    """
    The directory should contain exactly the three expected JSON files and
    nothing else (apart from '.' and '..' which the filesystem omits).
    This helps catch accidental extra files that could influence later steps.
    """
    expected_filenames = {p.name for p in EXPECTED_MANIFESTS}
    actual_filenames = {p.name for p in MANIFEST_DIR.iterdir() if p.is_file()}
    assert (
        actual_filenames == expected_filenames
    ), (
        f"Unexpected files found in {MANIFEST_DIR}.\n"
        f"Expected only: {sorted(expected_filenames)}\n"
        f"Found: {sorted(actual_filenames)}"
    )