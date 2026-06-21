FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create secrets directory hierarchy
RUN mkdir -p /home/user/secrets && \
    chmod 755 /home/user && \
    chmod 755 /home/user/secrets

# Populate credentials.csv
RUN cat <<'EOF' > /home/user/secrets/credentials.csv
app_name,username,password,last_rotated
billing-service,bill-user,B!llPass123,2022-12-01
auth-service,auth-user,Aut#2020,2023-04-15
reporting-service,rep-user,Rep0rt!,2022-11-20
legacy-api,legacy-user,L3gacyPwd,2022-01-10
EOF

# Set permissions for credentials file
RUN chmod 644 /home/user/secrets/credentials.csv

# Labels
# Author Credential-Rotation-Setup
# Description "Base container for credential-rotation exercise. Provides initial secrets directory and installs pytest."

# Environment setup
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN if [ -x /usr/bin/python3 ]; then \
        ln -sf /usr/bin/python3 /usr/local/bin/python || true ; \
    fi