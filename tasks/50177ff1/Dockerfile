FROM ubuntu:22.04

# Install Python, pytest, and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    coreutils && \
    pip install --no-cache-dir pytest

# Prepare filesystem layout
RUN mkdir -p /home/user && chmod 0777 /home/user

# Legacy helper script
RUN mkdir -p /home/user/legacy_scripts
RUN cat > /home/user/legacy_scripts/find_disabled_accounts.sh <<'EOF'
#!/usr/bin/env bash
# Simple legacy helper to list disabled usernames
if [ ! -f "$1" ]; then
    echo "usage: $0 <path-to-account-db>" >&2
    exit 1
fi
while IFS=: read -r user status; do
    if [ "$status" = "disabled" ]; then
        printf '%s\n' "$user"
    chmod 755 /home/user

    fi
done < "$1"
exit 0
EOF
RUN chmod 0755 /home/user/legacy_scripts/find_disabled_accounts.sh

# Accounts database file
RUN mkdir -p /home/user/legacy_data
RUN cat > /home/user/legacy_data/accounts.txt <<'EOF'
john:active
alice:disabled
bob:disabled
zoe:active
charlie:disabled
dave:active
EOF
RUN chmod 0644 /home/user/legacy_data/accounts.txt

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Labels
LABEL Author="task-setup"
LABEL Description="Container for disabled-accounts reporting exercise"

# Run script
RUN echo 'echo "Container for the disabled-accounts reporting exercise."' > /usr/local/bin/run.sh && \
    echo 'echo "Invoke an interactive shell to begin:  apptainer exec <image> /bin/bash"' >> /usr/local/bin/run.sh && \
    chmod +x /usr/local/bin/run.sh

CMD ["/usr/local/bin/run.sh"]