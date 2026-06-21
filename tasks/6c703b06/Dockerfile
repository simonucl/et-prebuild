# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and Pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create the non-root user "user"
RUN useradd -m -s /bin/bash user

# Build the required directory tree
RUN install -d -o user -g user /home/user/storage/logs/app1 && \
    install -d -o user -g user /home/user/storage/logs/app2/archive

# Create the .tmp files that must later be deleted
RUN touch /home/user/storage/logs/root.tmp && \
    touch /home/user/storage/logs/app1/upload.tmp && \
    touch /home/user/storage/logs/app1/session.tmp && \
    touch /home/user/storage/logs/app2/archive/cache.tmp && \
    touch /home/user/storage/logs/app2/archive/old_2021.tmp

# Create non-.tmp files that must remain intact
RUN touch /home/user/storage/logs/keep.log && \
    touch /home/user/storage/logs/app1/info.log && \
    touch /home/user/storage/logs/app2/error.log

# Ensure everything is owned by the non-root user and permissions are set
RUN chown -R user:user /home/user && \
    chmod -R u+rwX /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Labels
LABEL Author="example" \
      Description="Environment for log-cleanup task with pytest pre-installed"

# Default command
CMD ["/bin/bash"]