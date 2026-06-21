FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial directory structure
RUN mkdir -p /home/user/provisioning/logs

# Create provisioning.log
RUN cat > /home/user/provisioning/logs/provisioning.log <<'EOF'
2023-08-01 10:01:15 INFO: Starting provisioning sequence id=abc123
2023-08-01 10:01:20 WARN: Slow network detected, retries may occur
2023-08-01 10:01:25 ERROR: VM web-01 failed to boot in allotted time
2023-08-01 10:01:30 INFO: Attempting to recover VM web-01
2023-08-01 10:01:35 ERROR: Instance db-02 failed healthcheck after provisioning
2023-08-01 10:01:38 WARN: Provisioning latency above threshold
2023-08-01 10:01:40 INFO: Provisioning sequence id=abc123 completed with errors
EOF

# Permissions
RUN chmod -R a+rwx /home/user

# Labels
LABEL Author="Log-Filtering Task Setup" \
      Description="Provides the initial filesystem state and pytest for the log-filtering programming exercise."

# Help text
# This container supplies:
#   • Python 3 and pytest for automated assessment.
#   • /home/user/provisioning/logs/provisioning.log pre-populated with the required seven lines.
# No other artefacts are present so that the student can complete the task as specified.