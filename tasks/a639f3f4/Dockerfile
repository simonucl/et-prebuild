# From localimage is not supported in Docker, using closest base instead
FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/kube-operator/config

# Create configuration file via heredoc
RUN cat <<'EOF' > /home/user/kube-operator/config/app.ini
[staging]
app_name=my-web
image=example/my-web:v1.2.3
replicas=2
port=8080

[production]
app_name=my-web
image=example/my-web:v1.2.3
replicas=5
port=80
EOF

# Set permissions
RUN chmod 644 /home/user/kube-operator/config/app.ini && \
    chmod 755 /home/user /home/user/kube-operator /home/user/kube-operator/config

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD ["bash"]