FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state for the "permission-audit" task
# 1. Create the required directory hierarchy
RUN mkdir -p /home/user/permission_audit

# 2. Populate raw_permissions.txt with exactly 20 lines, preserving order
RUN cat > /home/user/permission_audit/raw_permissions.txt <<'EOF'
rwxr-xr-x
rw-r--r--
rwxr-xr-x
rw-r--r--
rw-r--r--
rwx------
rwxr-xr-x
rwx------
rwxr-xr-x
rw-r--r--
rwxr-xr-x
rwxr-xr--
rwxr-xr--
rw-r--r--
rwxr-xr--
rwxr-xr-x
rw-r--r--
rw-r--r--
rwxr-xr-x
rwxr-xr-x
EOF

# 3. Set permissive, non-root-only permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/permission_audit && \
    chmod 644 /home/user/permission_audit/raw_permissions.txt

CMD echo "This container is prepared for the 'permission-audit' exercise." && \
    echo "Navigate to /home/user/permission_audit to begin."