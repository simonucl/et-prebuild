FROM ubuntu:22.04

# Labels
LABEL Author="backup-task-prep"
LABEL Description="Initial state for Backup Integrity task – creates source tree and installs pytest."

# Post installation
RUN set -e && \
    echo "Updating apt repositories and installing dependencies..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip \
        ca-certificates \
        tar gzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest..." && \
    pip3 install --no-cache-dir --upgrade pip pytest

RUN echo "Creating initial directory structure and files..." && \
    mkdir -p /home/user/backup/source/documents && \
    mkdir -p /home/user/backup/source/images && \
    mkdir -p /home/user/backup/source/scripts && \
    mkdir -p /home/user/backup/source/data && \
    mkdir -p /home/user/backup/source/notes

# documents/report.txt
RUN cat > /home/user/backup/source/documents/report.txt <<'EOF'
Quarterly report Q1 2021
All figures in USD.
END
EOF

# images/logo.png (placeholder text line)
RUN printf "PNG_PLACEHOLDER\n" > /home/user/backup/source/images/logo.png

# scripts/backup.sh
RUN cat > /home/user/backup/source/scripts/backup.sh <<'EOF'
#!/usr/bin/env bash
# Simple maintenance script
echo "Backup completed."
EOF

RUN chmod +x /home/user/backup/source/scripts/backup.sh

# data/sample.csv
RUN cat > /home/user/backup/source/data/sample.csv <<'EOF'
id,name,score
1,Alice,83
2,Bob,91
3,Charlie,78
EOF

# notes/todo.md
RUN cat > /home/user/backup/source/notes/todo.md <<'EOF'
# TODO
- Verify backups
- Document retention policy
- Schedule incremental jobs
EOF

# Ensure all created directories are writable by the non-root user that will run the tests
RUN chmod -R a+rwX /home/user/backup && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD ["bash", "-c", "echo 'Container for Backup Integrity task. Open a shell to begin.' >&2 && exec /bin/bash"]

# Help information (as comments):
# This container provides the initial state for the Backup Integrity task.
# It includes the required source directory tree under /home/user/backup/source
# and has pytest pre-installed for the automated grader.