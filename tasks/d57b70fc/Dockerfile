FROM ubuntu:22.04

# Labels
LABEL Author="example_builder"
LABEL Description="Environment for FPS summary task – provides raw data file and pytest"

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the directory tree
RUN mkdir -p /home/user/perf/raw

# Populate the raw FPS sample file with ground-truth data
RUN cat >/home/user/perf/raw/fps_samples.log <<'EOF'
59
60
61
57
62
60
58
EOF

# Set permissions and create user
RUN chmod 777 /home/user/perf && \
    chmod 755 /home/user/perf/raw && \
    chmod 644 /home/user/perf/raw/fps_samples.log && \
    chmod 755 /home && \
    if ! getent passwd user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi

# Clean up APT caches to keep image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for FPS summary task.  See the assignment instructions for what to do next."]