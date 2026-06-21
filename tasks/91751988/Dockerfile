# Based on localimage bootstrap; using ubuntu:22.04 as base
FROM ubuntu:22.04

# Environment variables (empty in original %environment)
ENV HOME=/home/user

# %post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/doc_management && \
    chmod 755 /home/user/doc_management

RUN cat <<'SQL_END' > /tmp/init_documents.sql
CREATE TABLE documents(
    doc_id   INTEGER PRIMARY KEY,
    title    TEXT NOT NULL,
    category TEXT NOT NULL
);

INSERT INTO documents(doc_id, title, category) VALUES
    (1, 'Getting_Started', 'Guide'),
    (2, 'API_Reference',   'Reference'),
    (3, 'Release_Notes',   'Changelog');
SQL_END

RUN sqlite3 /home/user/doc_management/doc_index.db < /tmp/init_documents.sql && \
    rm /tmp/init_documents.sql && \
    chmod 644 /home/user/doc_management/doc_index.db

# %help section
# This container sets up the initial state for the documentation export task.
# It contains:
#   /home/user/doc_management directory
#   /home/user/doc_management/doc_index.db SQLite database with schema and rows
# Pytest is installed for the grading suite.

# %labels section
LABEL Author="ExampleAuthor"
LABEL Description="Environment for SQLite export task with pytest pre-installed."

# %runscript – approximated as CMD
CMD chmod 755 /home/user && \
    echo "Container for documentation export task." && \
    echo "Use a single SQLite command to create /home/user/doc_management/documents_export.csv as described."