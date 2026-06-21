FROM ubuntu:22.04

# Author credential-check-setup

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /home/user/projects/utils

# deploy.sh
RUN cat > /home/user/projects/deploy.sh <<'EOF'
#!/usr/bin/env bash
# Deploy script
db_password=secret123
echo "Deploying application..."
# END
EOF

# README.md
RUN cat > /home/user/projects/README.md <<'EOF'
Project documentation goes here.
EOF

# cleanup.sh
RUN cat > /home/user/projects/utils/cleanup.sh <<'EOF'
#!/usr/bin/env bash
 password =cleanme
password=cleanme2
echo "Cleanup completed"
EOF

# helper.sh
RUN cat > /home/user/projects/utils/helper.sh <<'EOF'
#!/usr/bin/env bash
echo "Helper"

passwd=letmein
EOF

# Permissions
RUN chmod 755 /home/user/projects/deploy.sh && \
    chmod 755 /home/user/projects/utils/cleanup.sh && \
    chmod 755 /home/user/projects/utils/helper.sh && \
    chmod 644 /home/user/projects/README.md

# Environment (none specified)