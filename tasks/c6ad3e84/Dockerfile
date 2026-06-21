# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/data/raw && \
    mkdir -p /home/user/scripts && \
    mkdir -p /home/user/logs

# Set permissions
RUN chmod 777 /home/user/scripts && \
    chmod 777 /home/user/logs

# Populate raw CSV fragments
RUN cat > /home/user/data/raw/raw_part1.csv << 'EOF'
id,text,label
1,"hello world",greeting
2,"how are you",question
3,"goodbye",farewell
EOF

RUN cat > /home/user/data/raw/raw_part2.csv << 'EOF'
id,text,label
4,"yes",affirmation
5,"no",negation
EOF

# Fix permissions for raw data
RUN chmod 644 /home/user/data/raw/raw_part*.csv && \
    chmod 755 /home/user/data/raw

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Help text (runscript equivalent)
# Container for the dataset-preparation task. Run `docker run -it <image> bash` for interactive session.