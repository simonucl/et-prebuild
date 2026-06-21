FROM ubuntu:22.04

# Update package lists and install required packages
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip parallel && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare INITIAL filesystem state expected by the automated tests
# ------------------------------------------------------------------
# Project root
RUN mkdir -p /home/user

# Incoming directory with the two raw CSV files (no headers)
RUN mkdir -p /home/user/incoming

RUN cat > /home/user/incoming/good_data.csv << 'EOF'
1,Alpha,2024-06-01T10:15:00Z,ACTIVE
2,Beta,2024-06-01T10:20:00Z,INACTIVE
3,Gamma,2024-06-01T10:25:00Z,ACTIVE
EOF

RUN cat > /home/user/incoming/bad_data.csv << 'EOF'
a,Delta,2024-06-01T11:00:00Z,ACTIVE
4,Epsilon,not-a-timestamp,INACTIVE
5,Zeta,2024-06-01T11:10:00Z,BROKEN
6,Eta,2024-06-01T11:15:00Z,ACTIVE
EOF

# Logs directory (must exist but remain empty)
RUN mkdir -p /home/user/logs

# Ensure no other directories/files that belong to the final solution exist
# (archive/, failed/, process_pipeline.sh, etc. must NOT be present)

# ------------------------------------------------------------------
# Permissions: make sure the non-root runtime user can work freely
# ------------------------------------------------------------------
RUN chmod -R 0775 /home/user && \
    find /home/user -type f -exec chmod 0664 {} \;

# Labels
LABEL Author="CSV-Pipeline-Starter"
LABEL Description="Initial state container for four-stage CSV pipeline assignment"

# Default command
CMD ["echo", "CSV pipeline starter container – no default run action."]