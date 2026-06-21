FROM ubuntu:22.04

# Update package index and install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create data directory structure
RUN mkdir -p /home/user/ml_data && \
    chmod 755 /home/user && \
    chmod 755 /home/user/ml_data

# Build the SQLite database
RUN sqlite3 /home/user/ml_data/training.db <<'SQL_EOF'
CREATE TABLE training_samples (
    id INTEGER PRIMARY KEY,
    text TEXT,
    label INTEGER
);
INSERT INTO training_samples (id,text,label) VALUES
    (1,'hello world',0),
    (2,'goodbye world',1),
    (3,'test sample',0);
SQL_EOF

# Set database file permissions
RUN chmod 644 /home/user/ml_data/training.db

# Adjust ownership
RUN chown -R 1000:1000 /home/user || true

# Ensure python symlink exists
RUN if [ -x /usr/bin/python3 ] && [ ! -e /usr/bin/python ]; then ln -s /usr/bin/python3 /usr/bin/python; fi

# Help text
# Author Machine-Learning Task Setup
# Description Sets up initial state for ML CSV export task with SQLite DB