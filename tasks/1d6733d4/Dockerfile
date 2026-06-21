FROM ubuntu:22.04

# Install Python tooling and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory structure for the task
RUN mkdir -p /home/user/mobile-pipelines/scripts && \
    mkdir -p /home/user/mobile-pipelines/logs

# Populate the scripts directory with the required files
# All script files are intentionally left non-executable (0644)
RUN cat <<'EOF' > /home/user/mobile-pipelines/scripts/deploy_android.sh
#!/usr/bin/env bash
# Placeholder script for deployment
echo "Deploying Android..."
EOF

RUN cat <<'EOF' > /home/user/mobile-pipelines/scripts/build_ios.sh
#!/usr/bin/env bash
# Placeholder script for iOS build
echo "Building iOS..."
EOF

RUN cat <<'EOF' > /home/user/mobile-pipelines/scripts/cleanup.sh
#!/usr/bin/env bash
# Placeholder cleanup script
echo "Cleaning up..."
EOF

# Non-script file that must remain untouched by the student
RUN echo "Utility scripts for the mobile pipelines project." \
    > /home/user/mobile-pipelines/scripts/readme.md

# Set initial permissions exactly as required
RUN chmod 0644 /home/user/mobile-pipelines/scripts/deploy_android.sh && \
    chmod 0644 /home/user/mobile-pipelines/scripts/build_ios.sh && \
    chmod 0644 /home/user/mobile-pipelines/scripts/cleanup.sh && \
    chmod 0644 /home/user/mobile-pipelines/scripts/readme.md

# Create the audit log file, initially empty
RUN touch /home/user/mobile-pipelines/logs/perm_fix.log && \
    chmod 0644 /home/user/mobile-pipelines/logs/perm_fix.log

# Set home directory permissions
RUN chmod 755 /home/user

CMD ["sh", "-c", "echo 'Container for Mobile Pipelines permission-fix exercise.' && echo 'Open a shell inside the container and execute your one-liner command.'"]