FROM ubuntu:22.04

# Help text
# This container provides the initial state for the link-creation exercise.
# It contains:
#   - /home/user/scripts/backup.sh (executable placeholder script)
# The student is expected to create /home/user/bin, a symbolic link, and a log file.
# Pytest is installed for automated grading.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip python3-setuptools && \
    pip3 install --no-cache-dir pytest

RUN install -d -m 0755 /home/user/scripts

RUN cat > /home/user/scripts/backup.sh <<'EOF'
#!/bin/bash
# Simple backup placeholder
echo "Backup running..."
exit 0
EOF

RUN chmod 0755 /home/user/scripts/backup.sh

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin"

# Run script message
# echo "Container for link-creation exercise is ready."
# echo "Run your commands or tests as needed."