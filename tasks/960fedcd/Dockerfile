# Converted from Apptainer definition file
FROM ubuntu:22.04

# %post section
RUN set -e && \
    echo "Updating package lists and installing Python tooling..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates && \
    echo "Installing pytest for the grading suite..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Setting up initial project structure..." && \
    mkdir -p /home/user/app

# Create requirements.txt via heredoc
RUN cat <<'EOF' >/home/user/app/requirements.txt
flask==2.2.0
requests==2.28.0
EOF

RUN chmod -R 0777 /home/user && \
    echo "Initial container setup complete."

# %environment section
RUN chmod 755 /home/user
ENV LC_ALL=C
ENV LANG=C

# %labels section
LABEL Author="ChatGPT"
LABEL Description="Base image for deployment-venv upgrade task; includes pytest and initial project layout."