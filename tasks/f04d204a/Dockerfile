FROM ubuntu:22.04

# Basic utilities and Python tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading suite
RUN pip3 install --no-cache-dir pytest

# Create the non-root user
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true

# Prepare the initial directory structure
RUN install -d -m 0755 /home/user/capacity_data

RUN cat > /home/user/capacity_data/server_usage.csv <<'EOF'
server_id,cpu_usage_pct,mem_usage_pct
s1,45,67
s1,55,65
s2,80,70
s2,60,75
s3,30,40
EOF

RUN chmod 0644 /home/user/capacity_data/server_usage.csv

# Ensure ownership
RUN chown -R 1000:1000 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV HOME=/home/user

# Apply chmod from %environment
RUN chmod 755 /home/user

CMD ["bash"]