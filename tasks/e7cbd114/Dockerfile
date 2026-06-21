FROM ubuntu:22.04

# Labels
LABEL Author="Example Builder"
LABEL Description="Environment for symlink migration task (pytest pre-state only)"

# Basic tooling
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the forthcoming test harness
RUN pip3 install --no-cache-dir pytest

# Prepare legacy filesystem state
# Create normal, *real* directories (not symlinks)
RUN mkdir -p /home/user/services/api && \
    mkdir -p /home/user/services/web

# Populate placeholder README files with the exact expected text
RUN printf "API service code lives here\n" > /home/user/services/api/README.txt && \
    printf "Web frontend code lives here\n" > /home/user/services/web/README.txt

# Ensure the /home/user tree is owned by an unprivileged user called 'user'
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/home/user/.local/bin:$PATH

# Default command
CMD ["/bin/bash"]