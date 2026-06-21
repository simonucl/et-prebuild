FROM ubuntu:22.04

# 1. Install system packages and pytest
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       python3 python3-venv python3-pip ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# 2. Create the filesystem layout
RUN mkdir -p /home/user/data

RUN cat > /home/user/data/backup_requirements.txt <<'EOF'
certifi==2023.7.22
charset-normalizer==3.3.2
idna==3.4
urllib3==2.0.7
requests==2.31.0
EOF

# 3. Permissions
RUN chmod 0777 /home/user && chmod -R a+r /home/user/data

# Environment variables from %environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8