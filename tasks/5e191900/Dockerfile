# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels
LABEL Author="Prepared by ChatGPT" \
      Description="Container image for TSV manipulation exercise with pytest pre-installed"

# Environment variables
ENV LANG=C \
    LC_ALL=C

# Install Python, pip, pytest, and certificates
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare directory layout
RUN mkdir -p /home/user/input && \
    mkdir -p /home/user/output

# Populate users_full.tsv
RUN cat > /home/user/input/users_full.tsv <<'EOF'
id	username	first_name	last_name	email	department	role	status
1001	alice	Alice	Smith	alice.smith@example.com	HR	MANAGER	ACTIVE
1002	bob	Bob	Jones	bob.jones@example.com	IT	SYSADMIN	INACTIVE
1003	carol	Carol	Taylor	carol.taylor@example.com	IT	SYSADMIN	ACTIVE
1004	dave	Dave	Wilson	dave.wilson@example.com	Finance	ACCOUNTANT	ACTIVE
1005	erin	Erin	Andrews	erin.andrews@example.com	IT	DEVELOPER	INACTIVE
EOF

# Populate new_roles.tsv
RUN cat > /home/user/input/new_roles.tsv <<'EOF'
alice	HR-LEAD
bob	DESKTOP-ADMIN
carol	SECURITY-ADMIN
dave	SENIOR-ACCOUNTANT
erin	FRONTEND-LEAD
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/input && \
    chmod 755 /home/user/output && \
    chmod 644 /home/user/input/users_full.tsv && \
    chmod 644 /home/user/input/new_roles.tsv

# Help:
# Container image for TSV manipulation exercise with pytest pre-installed