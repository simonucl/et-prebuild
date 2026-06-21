FROM ubuntu:22.04

# From %help:
# Container providing the initial state for the “MyApp” configuration-management
# exercise. pytest is pre-installed so test suites can run immediately.

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user

RUN echo '# .bashrc for user' > /home/user/.bashrc && \
    echo >> /home/user/.bashrc

RUN mkdir -p /home/user/myapp/bin && \
    mkdir -p /home/user/myapp/conf && \
    mkdir -p /home/user/bin

RUN cat > /home/user/myapp/bin/start.sh <<'EOF'
#!/bin/bash
echo "Starting MyApp"
EOF

RUN chmod 0755 /home/user/myapp/bin/start.sh

RUN cat > /home/user/myapp/conf/app.conf <<'EOF'
# MyApp Main configuration
log_level=INFO
max_threads=4
EOF

RUN chmod -R a+rX /home/user && \
    chmod -R u+w /home/user

# From %labels:
# Author "Apptainer Task Preparer"