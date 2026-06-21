FROM ubuntu:22.04

# Environment variables
ENV PATH=/usr/bin:$PATH

# Labels
LABEL Author="You"
LABEL Description="Environment for the database-migration task with pytest pre-installed."

# System setup and package installation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project && \
    chmod -R 0777 /home/user

# Create the SQLite database
RUN sqlite3 /home/user/project/old_app.db <<'SQL'
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
);
INSERT INTO users(id,name,email) VALUES
  (1,'Alice','alice@example.com'),
  (2,'Bob','bob@example.com'),
  (3,'Carol','carol@example.com');
SQL

# Set database permissions
RUN chmod 0666 /home/user/project/old_app.db && chmod 755 /home/user