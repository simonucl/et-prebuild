FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/data/backups

# Create CSV file
RUN cat > /home/user/data/backups/archive_2023-09-30.csv <<'CSV_EOF'
id,name,value
1,alpha,100
2,beta,200
3,gamma,300
CSV_EOF

# Create JSON metadata file
RUN cat > /home/user/data/backups/archive_2023-09-30.json <<'JSON_EOF'
{
  "header": ["id","name","value"],
  "rows": 3
}
JSON_EOF

# Create notes file
RUN echo "Backup created on 2023-09-30 at 03:00 UTC." > /home/user/data/backups/notes.txt

# Create manifest.json with computed hashes
RUN CSV_HASH=$(sha256sum /home/user/data/backups/archive_2023-09-30.csv | cut -d' ' -f1) && \
    NOTES_HASH=$(sha256sum /home/user/data/backups/notes.txt | cut -d' ' -f1) && \
    cat > /home/user/data/backups/manifest.json <<EOF
[
  {
    "file": "archive_2023-09-30.csv",
    "sha256": "${CSV_HASH}"
  },
  {
    "file": "notes.txt",
    "sha256": "${NOTES_HASH}"
  }
]
EOF

# Permissions
RUN chmod -R 0777 /home/user && chmod 755 /home/user

# Labels
LABEL Author="backup-verification-container"
LABEL Description="Environment prepared for the backup integrity validation task"

# Run script equivalent
CMD echo "Container for backup-verification task. Use docker exec to run commands."