FROM ubuntu:22.04

# Author: Apptainer build script for optimization-solver exercise
# Description: Provides initial environment, mock solver shim, and pytest

ENV PATH="/home/user/bin:$PATH"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/bin && \
    mkdir -p /home/user/solver_tests && \
    mkdir -p /home/user/solver_logs && \
    chmod 755 /home/user/bin /home/user/solver_tests /home/user/solver_logs

RUN cat << 'EOF' > /home/user/bin/mock_opt_solver
#!/usr/bin/env python3
import sys, json
_ = sys.stdin.read()
print(json.dumps({"objective": 123.45, "status": "OPTIMAL"}))
EOF

RUN chmod 755 /home/user/bin/mock_opt_solver

LABEL Author="Apptainer build script for optimization-solver exercise"
LABEL Description="Provides initial environment, mock solver shim, and pytest"