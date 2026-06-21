FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Build Script"
LABEL Description="Container for latency delta report task – seed logs + pytest"

# Update APT and install Python & pip
RUN set -e && \
    echo "Updating APT and installing Python & pip..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN echo "Installing pytest for the grader..." && \
    pip3 install --no-cache-dir pytest

# Setting up initial directory structure
RUN echo "Setting up initial directory structure and seed log files..." && \
    mkdir -p /home/user/logs

# Create serviceA log file
RUN cat > /home/user/logs/serviceA_2023-09-15.log <<'EOF'
2023-09-15T08:00:01Z|req-1001|u-501|120
2023-09-15T08:00:02Z|req-1002|u-502|95
2023-09-15T08:00:03Z|req-1003|u-503|230
2023-09-15T08:00:04Z|req-1004|u-504|110
2023-09-15T08:00:05Z|req-1005|u-505|150
EOF

# Create serviceB log file
RUN cat > /home/user/logs/serviceB_2023-09-15.log <<'EOF'
2023-09-15T08:00:01Z|req-1001|u-501|80
2023-09-15T08:00:02Z|req-1002|u-502|60
2023-09-15T08:00:03Z|req-1006|u-506|200
2023-09-15T08:00:04Z|req-1004|u-504|90
2023-09-15T08:00:05Z|req-1005|u-505|100
EOF

# Ensure correct permissions: directory writable, files read-only
RUN chmod 0777 /home/user/logs && \
    chmod 0644 /home/user/logs/serviceA_2023-09-15.log && \
    chmod 0644 /home/user/logs/serviceB_2023-09-15.log && \
    chmod 755 /home/user && \
    echo "Initial container setup complete."

# Environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /home/user