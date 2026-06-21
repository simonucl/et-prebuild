FROM ubuntu:22.04

# Labels
LABEL Author="devsecops-task-setup"
LABEL Description="Image pre-populated with INI files for remediation exercise"

# Post section
RUN set -eux && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Ensure a non-root user named "user" (UID 1000) exists
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 user; \
    fi

# Create the required directory structure
RUN install -d -m 0755 /home/user/policy/configs && \
    install -d -m 0755 /home/user/policy/reports

# Create app1.ini
RUN cat > /home/user/policy/configs/app1.ini << 'EOF'
[security]
enforce_tls=false

[logging]
level=DEBUG
EOF

# Create app2.ini
RUN cat > /home/user/policy/configs/app2.ini << 'EOF'
[security]
enforce_tls=true

[logging]
level=INFO
EOF

# Correct permissions and ownership
RUN chmod 0644 /home/user/policy/configs/app1.ini /home/user/policy/configs/app2.ini && \
    chown -R user:user /home/user/policy && \
    chmod 755 /home/user

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# Default command
CMD ["echo", "Container for DevSecOps INI remediation task. Invoke your tooling as needed."]