FROM ubuntu:22.04

# ------------------------------------------------------------------
# 1. Install required software
# ------------------------------------------------------------------
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools python3-wheel \
        iproute2 procps coreutils util-linux && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python testing framework
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# 2. Create non-root user "user"
# ------------------------------------------------------------------
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# ------------------------------------------------------------------
# 3. Seed repository data under /opt/binaries
# ------------------------------------------------------------------
RUN mkdir -p /opt/binaries/archives && \
    chmod 755 /opt/binaries /opt/binaries/archives && \
    fallocate -l 40M /opt/binaries/widget-1.0.0.tar.gz && \
    fallocate -l 25M /opt/binaries/gadget-2.5.1.zip && \
    fallocate -l 12M /opt/binaries/libfoo.so && \
    fallocate -l 60M /opt/binaries/archives/legacy.bin && \
    chmod 644 /opt/binaries/widget-1.0.0.tar.gz \
              /opt/binaries/gadget-2.5.1.zip \
              /opt/binaries/libfoo.so \
              /opt/binaries/archives/legacy.bin && \
    chmod -R o+r /opt/binaries

# ------------------------------------------------------------------
# 4. Ensure home directory ownership
# ------------------------------------------------------------------
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# NOTE: /home/user/diagnostics is intentionally **not** created so that
#       the student must create it, satisfying the test conditions.

# Set working directory
WORKDIR /home/user

# Start an interactive shell by default
CMD ["/bin/bash"]