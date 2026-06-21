# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Basic utilities and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates \
        tar \
        gzip && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user `user`
RUN id -u user >/dev/null 2>&1 || useradd -m -u 1000 user

# Set up directory tree and sample log files
RUN install -d -m 0755 /home/user/mobile_ci/pipeline_reports && \
    install -d -m 0755 /home/user/mobile_ci/archives && \
    echo "Compilation completed successfully." > /home/user/mobile_ci/pipeline_reports/compile.log && \
    echo "All 128 unit tests passed."         > /home/user/mobile_ci/pipeline_reports/unit_test.log && \
    echo "Integration suite finished OK."     > /home/user/mobile_ci/pipeline_reports/integration_test.log && \
    chown -R 1000:1000 /home/user

# Apply chmod from %environment
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Labels
LABEL Author="task-preparer=Apptainer Assistant"
LABEL Description="Environment for mobile CI archiving task with pytest pre-installed."