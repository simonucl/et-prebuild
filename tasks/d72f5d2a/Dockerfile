FROM ubuntu:22.04

# Labels
LABEL Author="task-generator"
LABEL Description="Container for ML optimiser data-prep task – provides initial raw_dataset.csv and pytest."

# Post installation
RUN set -e && \
    echo "Updating apt repositories..." && \
    apt-get update -qq && \
    echo "Installing Python and pip..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "Installing pytest via pip..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    echo "Creating /home/user directory and raw CSV..." && \
    mkdir -p /home/user

# Create the raw_dataset.csv with header + 5 data rows
RUN cat > /home/user/raw_dataset.csv <<'EOF'
id,feature1,feature2,label
1,5.1,3.5,0
2,4.9,3.0,0
3,6.2,3.4,1
4,5.9,3.0,1
5,6.0,3.2,1
EOF

# Ensure correct permissions
RUN chmod 644 /home/user/raw_dataset.csv && \
    chmod 755 /home/user && \
    echo "Setup complete."

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD echo "This container is prepared for the optimiser data-prep task." && \
    echo "Open a shell inside the container and follow the task instructions."