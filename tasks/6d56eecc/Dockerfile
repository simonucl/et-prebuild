FROM ubuntu:22.04

# Install Python 3 + pip and other dependencies
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create a helper script that prepares the initial challenge state
RUN cat >/usr/local/bin/_init_firewall_state.sh <<'EOF'
#!/bin/sh
FWDIR="/home/user/firewall"
RULES="$FWDIR/current_rules.list"

# Make sure the directory exists and is writable
mkdir -p "$FWDIR"

# If the base rules file is missing, create it with the exact contents
if [ ! -f "$RULES" ]; then
    cat >"$RULES" <<'EOR'
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
EOR
fi

# Do NOT create the files that the learner is supposed to generate later
exit 0
EOF

RUN chmod +x /usr/local/bin/_init_firewall_state.sh

# Create user and set up home directory
RUN useradd -m -s /bin/bash user && \
    chmod 755 /home/user

# Set environment variables
ENV PATH="/usr/local/bin:$PATH"

# Create entrypoint script to initialize state on container start
RUN cat >/usr/local/bin/entrypoint.sh <<'EOF'
#!/bin/sh
/usr/local/bin/_init_firewall_state.sh >/dev/null 2>&1 || true
exec "$@"
EOF

RUN chmod +x /usr/local/bin/entrypoint.sh

# Labels
LABEL Author="firewall-exercise"

# Help information (as comment)
# This container sets up the initial filesystem state for the
# "firewall rules" command-line exercise and includes pytest for grading.

WORKDIR /home/user
USER user

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/bin/bash"]