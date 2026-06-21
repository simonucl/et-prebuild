FROM ubuntu:22.04

# Set UTF-8 locale to avoid encoding surprises
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install Python & pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial workspace
# Create the user's home directory with permissive rights so the
# non-root agent running the tests can write into it later on.
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Set up /home/user/data with the required source files
RUN mkdir -p /home/user/data && \
    chmod 0755 /home/user/data

# Create alpha.txt
RUN cat > /home/user/data/alpha.txt <<'EOF'
Hello Alpha
EOF

# Create beta.txt
RUN cat > /home/user/data/beta.txt <<'EOF'
Beta line1
Beta line2
EOF

# Ensure correct permissions for files
RUN chmod 0644 /home/user/data/alpha.txt && \
    chmod 0644 /home/user/data/beta.txt && \
    chmod 755 /home/user

# Clean up APT cache
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Labels
LABEL Author="backup-exercise-builder"
LABEL Description="Environment for backup archiving exercise with pytest pre-installed."

# Help information (as comment):
# This image provides the initial state required for the
# "backup administrator" exercise. The student will create
# /home/user/archive/data_backup.tar.gz and update
# /home/user/archive/backup_record.log during the assessment.