FROM ubuntu:22.04

# Install Python, pip, and certificates
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/build-logs

# Create reference log file
RUN cat > /home/user/build-logs/release_2023-05-18.log <<'EOF'
[2023-05-18 14:22:01] [INFO]  [compile] Compilation successful
[2023-05-18 14:22:05] [WARN]  [test]    Unit test took longer than expected
[2023-05-18 14:22:10] [ERROR] [compile] Missing semicolon in source/foo.c
[2023-05-18 14:22:15] [INFO]  [package] Packaging artifacts
[2023-05-18 14:22:20] [ERROR] [deploy]  Cannot connect to production server
[2023-05-18 14:22:25] [INFO]  [deploy]  Connection re-established
[2023-05-18 14:22:30] [ERROR] [deploy]  Deployment aborted due to previous errors
[2023-05-18 14:22:35] [INFO]  [cleanup] Temporary files removed
[2023-05-18 14:22:40] [WARN]  [deploy]  Retrying deployment
[2023-05-18 14:22:45] [ERROR] [deploy]  Retry failed, manual intervention required
EOF

# Set permissions
RUN chmod 755 /home/user /home/user/build-logs && \
    chmod 644 /home/user/build-logs/release_2023-05-18.log

# Environment variables
ENV PATH="/usr/bin:$PATH"

# Labels
LABEL Author="Automated build for task: filter deploy errors"
LABEL Description="Provides the initial state and pytest for the log-filtering task."