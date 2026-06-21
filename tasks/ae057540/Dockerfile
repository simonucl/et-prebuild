# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# From %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/projects/mobile-ci

RUN cat > /home/user/projects/mobile-ci/pipeline_runs.csv <<'EOF'
20231015-001;android;main;SUCCESS
20231015-002;android;main;FAILURE
20231015-003;ios;main;SUCCESS
20231015-004;ios;develop;FAILURE
20231015-005;ios;develop;SUCCESS
20231015-006;android;develop;SUCCESS
20231015-007;ios;develop;FAILURE
20231015-008;android;main;SUCCESS
20231015-009;android;main;SUCCESS
20231015-010;ios;develop;FAILURE
EOF

RUN chmod -R 0777 /home/user

# From %environment
RUN chmod 755 /home/user
ENV LANG=C
ENV LC_ALL=C

# From %labels
LABEL Author="Apptainer Build Automation"
LABEL Description="Starter container for the mobile CI maintenance task"