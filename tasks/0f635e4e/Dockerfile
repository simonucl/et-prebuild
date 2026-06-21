FROM ubuntu:22.04

# Labels
LABEL Author="security-auditor-setup"
LABEL Description="Environment for permission-frequency audit task with pytest pre-installed."

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV DEBIAN_FRONTEND=noninteractive

# Basic tools and Python with pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create /home/user with open write permissions
RUN mkdir -p /home/user && \
    chmod 777 /home/user

# Directory that stores the provided permissions snapshot
RUN mkdir -p /home/user/audit_samples && \
    chmod 755 /home/user/audit_samples

# Populate the snapshot file exactly as specified
RUN cat > /home/user/audit_samples/perms_report.txt <<'EOF'
-rwxr-xr-x
-rw-r--r--
drwxr-xr-x
-rwxr-xr-x
-rw-------
drwxr-x---
-rwxr-xr-x
-rw-r--r--
-rw-r--r--
drwxr-xr-x
EOF

# Ensure correct permissions: world-readable, but not writable
RUN chmod 644 /home/user/audit_samples/perms_report.txt