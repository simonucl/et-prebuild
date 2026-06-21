FROM ubuntu:22.04

# Basic tools required for the uptime-monitoring exercise
RUN set -eux && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive \
        apt-get install -y --no-install-recommends \
            python3 \
            python3-pip \
            curl \
            iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Create the unprivileged runtime user (uid/gid 1000) expected by tests
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# Ensure HOME exists and has correct ownership
RUN mkdir -p /home/user && \
    chown 1000:1000 /home/user && \
    chmod 755 /home/user

# Keep standard PATH and prepend common locations
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default entry: drop into a shell as-is
CMD ["/bin/bash"]