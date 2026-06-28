FROM ubuntu:24.04

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs
WORKDIR /app

# Tools the agent may use; nothing here solves the task.
RUN apt-get update && apt-get install -y --no-install-recommends \
        coreutils python3 jq ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create the unprivileged working user expected by the scenario.
RUN id user >/dev/null 2>&1 || useradd -m -s /bin/bash user

# ---------------------------------------------------------------------------
# Stage the STARTING state: a directory of build artifacts with DETERMINISTIC
# byte content (so SHA-256 and sizes are fixed). File names embed the classic
# numeric-vs-lexical version trap (1.10.0 > 1.9.0 ; 0.1.12 > 0.1.2 ; 2.0.10 > 2.0.9).
# ---------------------------------------------------------------------------
RUN set -eu; \
    inc=/home/user/artifacts/incoming; \
    mkdir -p "$inc"; \
    # helper: write N copies of a tag so files have distinct, fixed sizes
    mk() { f="$1"; n="$2"; tag="$3"; : > "$inc/$f"; i=0; while [ "$i" -lt "$n" ]; do printf '%s\n' "$tag" >> "$inc/$f"; i=$((i+1)); done; }; \
    # redis (tar.gz), two arches, 1.9.0 vs 1.10.0
    mk "redis-1.9.0-x86_64.tar.gz"    7  "redis-1.9.0-x86_64"; \
    mk "redis-1.10.0-x86_64.tar.gz"  11  "redis-1.10.0-x86_64"; \
    mk "redis-1.9.0-aarch64.tar.gz"   5  "redis-1.9.0-aarch64"; \
    mk "redis-1.10.0-aarch64.tar.gz"  9  "redis-1.10.0-aarch64"; \
    # nginx (tar.zst), x86_64, 2.0 vs 2.0.9 vs 2.0.10
    mk "nginx-2.0-x86_64.tar.zst"     3  "nginx-2.0-x86_64"; \
    mk "nginx-2.0.9-x86_64.tar.zst"  13  "nginx-2.0.9-x86_64"; \
    mk "nginx-2.0.10-x86_64.tar.zst"  6  "nginx-2.0.10-x86_64"; \
    # libfoo (whl), aarch64, 0.1 vs 0.1.2 vs 0.1.12
    mk "libfoo-0.1-aarch64.whl"       4  "libfoo-0.1-aarch64"; \
    mk "libfoo-0.1.2-aarch64.whl"    10  "libfoo-0.1.2-aarch64"; \
    mk "libfoo-0.1.12-aarch64.whl"    8  "libfoo-0.1.12-aarch64"; \
    chown -R user:user /home/user/artifacts

USER user
WORKDIR /home/user
