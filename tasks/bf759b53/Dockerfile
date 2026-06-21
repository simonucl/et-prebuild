# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# From %post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/provisioning

RUN cat >/home/user/provisioning/hosts.txt <<'EOF'
web01
db01
web01
web02
db01
app01
web02
web02
db01
EOF

RUN chmod -R a+rwx /home/user

# From %labels section
LABEL Author="Apptainer Task Prep"
LABEL Description="Environment for hostname frequency summarization task with pytest available."

# From %help section
# This container provides the initial state for the hostname frequency
# summarization task. It contains:
#   - /home/user/provisioning/hosts.txt – the raw host list.
#   - pytest – installed system-wide for automated grading.
# No output file has been pre-created; the student must generate
# /home/user/provisioning/host_frequencies.log as specified.