FROM ubuntu:22.04

# Labels
LABEL Author="Container prepared for Unix column-manipulation task"
LABEL Description="Provides starting state and pytest installation for automated grading."

# Post installation commands
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Create the dedicated non-root account expected by the tasks/tests
RUN useradd -m -s /bin/bash user

# Inventory directory and starting CSV file
RUN install -d -m 755 /home/user/inventory

RUN cat > /home/user/inventory/ssh_audit.csv <<'EOF'
serverName,port,permitRootLogin,protocol,extra
alpha,22,yes,2,ok
beta,2222,no,2,deprecated
gamma,22,prohibit-password,2,ok
delta,22,no,2,ok
epsilon,2200,yes,2,legacy
EOF

RUN chmod 644 /home/user/inventory/ssh_audit.csv

# Ensure ownership so that the non-root user can read the starting files
RUN chown -R user:user /home/user

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Help information (as comment)
# This container image bootstraps the environment for the "Unix column-manipulation"
# exercise. It pre-installs pytest (used by the autograder) and places the required
# starting CSV data in /home/user/inventory.