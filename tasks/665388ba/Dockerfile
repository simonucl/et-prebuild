# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial filesystem state expected by the tests
# ------------------------------------------------------------------

# 1. Create the sample application log with the required contents
RUN mkdir -p /home/user/sample_app/logs && \
    cat > /home/user/sample_app/logs/app.log <<'EOF'
[2023-07-01 12:01:22] INFO User login successful
[2023-07-01 12:03:11] WARNING Disk usage at 81%
    chmod 755 /home/user

[2023-07-01 12:05:47] ERROR Failed to open /etc/passwd for writing
[2023-07-01 12:06:58] CRITICAL Unauthorized access attempt detected from 10.0.0.5
[2023-07-01 12:07:15] INFO Session terminated
[2023-07-01 12:10:02] ERROR SQL injection attempt blocked
[2023-07-01 12:12:33] ERROR Invalid user token
[2023-07-01 12:16:30] INFO Background job started
[2023-07-01 12:17:13] CRITICAL Buffer overflow in module auth.so
[2023-07-01 12:18:49] INFO Background job finished
[2023-07-01 12:22:11] ERROR Cannot establish TLS handshake
[2023-07-01 12:25:55] CRITICAL Root privilege escalation attempt
[2023-07-01 12:28:37] INFO User logout
[2023-07-01 12:30:04] ERROR Access denied for user 'guest'
[2023-07-01 12:33:27] WARNING Memory usage at 72%
[2023-07-01 12:35:42] CRITICAL Data tampering detected
[2023-07-01 12:37:00] INFO Cron job executed
[2023-07-01 12:40:18] ERROR Malformed input received
[2023-07-01 12:41:59] INFO Cron job completed
[2023-07-01 12:45:22] CRITICAL SELinux policy violation
EOF

# 2. Make sure everything is readable and /home/user is writeable
RUN chmod -R a+r /home/user/sample_app && \
    chmod 0777 /home/user

LABEL Author="monitoring-specialist-bot" \
      Description="Base image for security-alert workflow task. Contains sample log and pytest."

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This image provides the initial state for the security-alert workflow task.
# A sample log file is placed at:
#   /home/user/sample_app/logs/app.log
# and pytest is installed so the exercise test suite can run.
#
# The directory /home/user is made writeable so that the learner’s code can
# create /home/user/alerts/security_alert.json during evaluation.