# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from Apptainer %help
# This Apptainer image provides the initial filesystem state and all tools
# (Python, pip, pytest, jq) that students need to complete the “API regression-test”
# assignment. The directory /home/user/projects/api-test contains the prepared
# input files and an empty output directory; the schema file is intentionally
# absent so that students can create it as part of their solution.

LABEL Author="ChatGPT"
LABEL Description="Environment for automated regression-test exercise (API JSON validation)"
LABEL Stage="initial-state ready for student"

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating apt repositories and installing required packages ..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        jq \
        ca-certificates \
        && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "Installing pytest (used by the automated grader) ..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    echo "Creating initial directory structure for the API regression-test exercise ..." && \
    mkdir -p /home/user/projects/api-test/input && \
    mkdir -p /home/user/projects/api-test/output && \
    mkdir -p /home/user/projects/api-test/schema

RUN cat <<'EOF' > /home/user/projects/api-test/input/user1.json
{
  "id": 101,
  "name": "Alice Smith",
  "email": "alice@example.com",
  "isActive": true
}
EOF

RUN cat <<'EOF' > /home/user/projects/api-test/input/user2.json
{
  "id": 102,
  "name": "Bob Jones",
  "isActive": false
}
EOF

RUN chmod -R a+rwX /home/user

RUN chmod 755 /home/user