FROM ubuntu:22.04

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create initial project structure
RUN mkdir -p /home/user/project/i18n

# Generate initial en.yaml
RUN cat > /home/user/project/i18n/en.yaml <<'EOF'
# English (United States) translations
welcome: "Welcome"
login: "Log in"
profile: "Profile"
settings: "Settings"
help: "Help"
EOF

# Generate initial config.toml
RUN cat > /home/user/project/config.toml <<'EOF'
# Project build configuration
[translations]
supported = 5           # number of keys in the en.yaml catalogue

[meta]
last_updated = "2023-09-01"
EOF

# Set required permissions
RUN chmod 0644 /home/user/project/i18n/en.yaml && \
    chmod 0644 /home/user/project/config.toml && \
    chmod 0755 /home/user/project/i18n && \
    chmod 0755 /home/user/project

# Permissions for /home/user from %environment
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

LABEL Author="ChatGPT - Apptainer prep"
LABEL Description="Container with initial state for localization update task"