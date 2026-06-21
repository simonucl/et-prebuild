FROM ubuntu:22.04

# Author Integration-Dev Challenge
# Description Container for optimisation-solver logging task – includes initial JSON payload and pytest installed.
# This image provides the starting environment for the optimisation-solver logging task.
# It already contains:
#   - /home/user/api_test/solver_response.json (mock API reply)
# Pytest is pre‑installed for automated grading.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip jq && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux && \
    mkdir -p /home/user/api_test

RUN cat > /home/user/api_test/solver_response.json <<'JSON_EOF'
{
  "status": "optimal",
  "x": [1.5, 0.0, 2.5],
  "objective_value": -7.25,
  "solver_time_sec": 0.003
}
JSON_EOF

RUN chmod 644 /home/user/api_test/solver_response.json

RUN chmod 755 /home/user