# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help text
# This container provides the initial filesystem state and Python tooling
# required for the “flat-text user database” task.

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create initial filesystem state
RUN set -e && \
    BASE_DIR="/home/user/site_users" && \
    mkdir -p "${BASE_DIR}"

# users.db
RUN cat > /home/user/site_users/users.db <<'EOF'
alice:active:alice@example.com
bob:active:bob@example.com
carol:disabled:carol@oldmail.com
dave:active:dave@example.com
EOF

# pending_additions.txt
RUN cat > /home/user/site_users/pending_additions.txt <<'EOF'
eve eve@example.com
frank frank@example.com
carol carol@newmail.com
EOF

# pending_deactivations.txt
RUN cat > /home/user/site_users/pending_deactivations.txt <<'EOF'
bob
frank
EOF

# pending_email_updates.txt
RUN cat > /home/user/site_users/pending_email_updates.txt <<'EOF'
alice alice@newdomain.com
carol carol@newdomain.com
EOF

# Permissions
RUN chmod -R a+rwX /home/user/site_users

# Environment settings
ENV HOME=/home/user
RUN chmod 755 /home/user

# Labels
LABEL Author="your_name_here"
LABEL Description="Environment for flat-text user database exercise with pytest pre-installed."