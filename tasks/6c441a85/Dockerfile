# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="core-dump-task-generator" \
      Description="Environment for core-dump compression exercise"

# ------------------------------------------------------------------
# Install required tooling and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        gzip \
        findutils \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare the initial filesystem state expected by the exercise
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/app_dumps && \
    printf 'CORE_DUMP_1\n'         > /home/user/app_dumps/crash1.core && \
    printf 'CORE_DUMP_2\n'         > /home/user/app_dumps/crash2.core && \
    printf 'CORRUPTED_CORE_DUMP\n' > /home/user/app_dumps/crash3.core && \
    chmod 777 /home/user && \
    chmod 777 /home/user/app_dumps && \
    chmod 666 /home/user/app_dumps/*.core && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables (from %environment)
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# ------------------------------------------------------------------
# Runtime behavior (from %runscript)
# ------------------------------------------------------------------
CMD ["/bin/bash", "-c", "echo \"Container for the core-dump compression exercise.\" && echo \"Enter the shell to begin:\" && exec /bin/bash"]