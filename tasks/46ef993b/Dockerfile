FROM ubuntu:22.04

# Update base system and install Python & pytest
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip --no-install-recommends && \
    pip3 install --no-cache-dir pytest

# Prepare initial project documentation under /home/user/docs
RUN mkdir -p /home/user/docs

# setup.md
RUN cat <<'EOF' > /home/user/docs/setup.md
# Project Setup
Please set the API_KEY environment variable before running.
EOF

# credentials.md
RUN cat <<'EOF' > /home/user/docs/credentials.md
# Credentials
Do not hardcode passwords in source code.
Store secrets in environment variables.
EOF

# readme.md
RUN cat <<'EOF' > /home/user/docs/readme.md
# Welcome
This project uses open data.
EOF

# Adjust permissions
RUN chmod -R 755 /home/user && \
    find /home/user/docs -type f -exec chmod 644 {} \;

# Environment setup
RUN chmod 755 /home/user
ENV PATH="$PATH:~/.local/bin"

# Labels
LABEL Author="AI Generated"
LABEL Description="Environment for security-phrase scan task with pytest pre-installed."