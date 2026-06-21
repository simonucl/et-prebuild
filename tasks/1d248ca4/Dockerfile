FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create dedicated unprivileged user “user”
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g user -s /bin/bash user

# Prepare initial repository layout
RUN mkdir -p /home/user/binary-repo && \
    touch /home/user/binary-repo/alpha-1.0.0.jar && \
    touch /home/user/binary-repo/alpha-1.0.1.jar && \
    touch /home/user/binary-repo/beta-2.2.3.tmp && \
    touch /home/user/binary-repo/gamma-0.9.1.partial && \
    touch /home/user/binary-repo/readme.txt && \
    chmod 755 /home/user/binary-repo && \
    chmod 644 /home/user/binary-repo/* && \
    chmod 777 /home/user

# Lightweight crontab wrapper
RUN cat << 'EOF' > /usr/local/bin/crontab
#!/usr/bin/env bash
# Minimal crontab replacement for containerised training environments.
# Stores the per-user crontab in $HOME/.crontab

CRON_FILE="${HOME}/.crontab"

usage() {
    echo "Usage: crontab [-l] [file|-]" >&2
    exit 1
}

if [[ "$#" -eq 1 && "$1" == "-l" ]]; then
    if [[ -f "$CRON_FILE" ]]; then
        cat "$CRON_FILE"
        exit 0
    else
        echo "no crontab for $(whoami)" >&2
        exit 1
    fi
elif [[ "$#" -eq 1 && "$1" == "-" ]]; then
    # Read new crontab from STDIN
    cat > "$CRON_FILE"
    exit 0
elif [[ "$#" -eq 1 ]]; then
    # Install crontab from file
    if [[ -f "$1" ]]; then
        cp "$1" "$CRON_FILE"
        exit 0
    else
        echo "crontab: cannot open $1: No such file" >&2
        exit 1
    fi
else
    usage
fi
EOF
RUN chmod 755 /usr/local/bin/crontab

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

# Help (as comments)
# Author Artifact-Manager Task Setup
# Description Base container for the “artifact–manager” exercise.
# Creates the initial binary repository under /home/user/binary-repo and
# installs pytest plus a lightweight user-level crontab replacement.

CMD ["/bin/bash"]