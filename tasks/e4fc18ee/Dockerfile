FROM ubuntu:22.04

# Help documentation:
# This container provides the starting environment for the
# web-analytics CSV reporting assignment.  It contains:
#   • The required directory structure and sample visits.csv dataset
#   • Python 3 with pytest pre-installed for validation
# Students should write their solution commands after starting a shell
# inside this container.

# Update package lists and install Python tooling
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create an unprivileged user that will own the project files
RUN useradd -m -s /bin/bash user || true

# Prepare the initial filesystem state expected by the tests
RUN mkdir -p /home/user/projects/webapp/data && \
    mkdir -p /home/user/projects/webapp/reports

# Populate the CSV dataset with the exact required content
RUN cat > /home/user/projects/webapp/data/visits.csv <<'EOF'
date,user_id,browser,status
2024-05-01,101,Chrome,200
2024-05-01,102,Firefox,200
2024-05-01,103,Chrome,404
2024-05-02,104,Chrome,200
2024-05-02,105,Edge,200
2024-05-03,106,Chrome,200
EOF

# Set permissions: directories world-readable/executable, CSV world-readable
RUN chmod -R 755 /home/user/projects && \
    chmod 644 /home/user/projects/webapp/data/visits.csv && \
    chown -R user:user /home/user/projects /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash", "-c", "echo 'Container for the web-analytics reporting task.' && echo 'Run your commands inside an interactive shell.'"]