# test_initial_state.py
#
# This test-suite validates that the system state **before** the student
# begins work is sane.  It deliberately avoids looking for any artefacts
# the student is expected to create later.
#
# What we *do* check:
#   • The optimization-solver shim binary exists and is executable.
#   • Invoking that binary yields the exact, well-formed JSON reply the
#     task description promises (“objective” float and “status” string).
#
# If any of these assertions fail, the learner’s environment is broken
# before they even start, and the failure message will point to the
# missing or mis-configured piece.

import json
import os
import subprocess
import sys
import pathlib
import stat
import pytest

# Absolute path to the solver shim that must already exist.
SOLVER_BIN = "/home/user/bin/mock_opt_solver"

@pytest.mark.describe("Initial environment sanity checks")
class TestInitialState:
    def test_solver_binary_exists_and_is_executable(self):
        """
        The solver shim must exist at the expected path and have the executable
        permission bit set for the current user.
        """
        if not os.path.isfile(SOLVER_BIN):
            pytest.fail(
                f"Expected solver binary not found at '{SOLVER_BIN}'. "
                "Make sure the provisioning step placed it there."
            )

        # Ensure current user has execute permission.
        if not os.access(SOLVER_BIN, os.X_OK):
            mode = oct(os.stat(SOLVER_BIN).st_mode)[-3:]
            pytest.fail(
                f"Solver binary exists but is not executable (mode {mode}). "
                "Please adjust its permissions (e.g., chmod +x)."
            )

    def test_solver_produces_expected_json_shape_and_values(self):
        """
        Running the binary with *any* JSON input should instantly return the
        canonical JSON reply documented in the task description.  We validate:
          • Exit code is zero.
          • STDOUT is exactly one JSON object.
          • The object contains the correct keys and expected values.
        """
        dummy_request = b'{"dummy": "data"}\n'
        try:
            cp = subprocess.run(
                [SOLVER_BIN],
                input=dummy_request,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=5,
            )
        except FileNotFoundError:
            pytest.fail(
                f"Could not execute '{SOLVER_BIN}'. "
                "Is the file missing or the path incorrect?"
            )
        except PermissionError:
            pytest.fail(
                f"Permission denied when executing '{SOLVER_BIN}'. "
                "Ensure it has execute permissions."
            )

        if cp.returncode != 0:
            pytest.fail(
                f"Solver process exited with non-zero status {cp.returncode}. "
                f"STDERR was: {cp.stderr.decode(errors='ignore')!r}"
            )

        stdout_text = cp.stdout.decode().strip()
        if not stdout_text:
            pytest.fail("Solver produced no output on STDOUT.")

        # The solver is supposed to emit a *single line* JSON document.
        try:
            reply = json.loads(stdout_text)
        except json.JSONDecodeError as exc:
            pytest.fail(
                f"Solver output was not valid JSON: {stdout_text!r}\n{exc}"
            )

        expected_keys = {"objective", "status"}
        if set(reply.keys()) != expected_keys:
            pytest.fail(
                f"Solver JSON keys mismatch. Expected {expected_keys}, "
                f"got {set(reply.keys())}."
            )

        # Validate data types.
        if not isinstance(reply["objective"], (float, int)):
            pytest.fail(
                "Solver 'objective' field is not numeric "
                f"(got type {type(reply['objective']).__name__})."
            )
        if not isinstance(reply["status"], str):
            pytest.fail(
                "Solver 'status' field is not a string "
                f"(got type {type(reply['status']).__name__})."
            )

        # Validate the exact values promised by the provisioning script.
        if reply["objective"] != 123.45 or reply["status"] != "OPTIMAL":
            pytest.fail(
                "Solver reply values differ from the expected ground truth.\n"
                f"Received: {reply}\nExpected: "
                "{'objective': 123.45, 'status': 'OPTIMAL'}"
            )