FROM ubuntu:22.04

# Install Python and pytest for the validation suite
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/logs

# Allow the (non-root) runtime user to create /home/user/cert_debug later
RUN chmod 0777 /home/user

# Populate the ssl_error.log with the exact required contents
RUN cat > /home/user/logs/ssl_error.log <<'EOF'
[2024-02-01 10:15:20] ERROR tls: certificate verify failed for domain example.com
[2024-02-01 10:20:50] ERROR tls: certificate verify failed for domain api.example.com
[2024-02-01 11:00:05] ERROR tls: certificate verify failed for domain example.com
[2024-02-01 11:30:00] INFO handshake succeeded for domain good.com
[2024-02-01 12:45:35] ERROR tls: certificate verify failed for domain test.site
[2024-02-01 13:00:00] ERROR tls: certificate verify failed for domain api.example.com
EOF

RUN chmod 0644 /home/user/logs/ssl_error.log && \
    chmod 0755 /home/user/logs

# Author: devops-task-prep
# Description: "Initial state for certificate failure summary task"

# Help:
# This container sets up the starting environment for the certificate-failure
# summary exercise. It includes pytest (for automated grading) and the pre-filled
# log file at /home/user/logs/ssl_error.log. The /home/user/cert_debug directory
# is intentionally absent so the learner can create it during the task.