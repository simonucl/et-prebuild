FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT-generated definition file"
LABEL Description="Environment for the 'Alice open tickets' SQLite/CSV export task"

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        sqlite3 \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/helpdesk

# Create the SQLite database with the required schema and rows
RUN sqlite3 /home/user/helpdesk/tickets.db <<'SQL'
CREATE TABLE tickets (
    id       INTEGER PRIMARY KEY,
    title    TEXT,
    assignee TEXT,
    status   TEXT,
    priority TEXT
);
INSERT INTO tickets (id, title, assignee, status, priority) VALUES
    (1, 'Email not working', 'Alice',   'open',   'High'),
    (2, 'VPN issue',         'Bob',     'closed', 'Medium'),
    (3, 'Computer hangs',    'Alice',   'open',   'Low'),
    (4, 'Printer offline',   'Charlie', 'open',   'Medium'),
    (5, 'Password reset',    'Alice',   'closed', 'Low');
SQL

# Ensure non-root users can read the database and write the output CSV
RUN chmod 777 /home/user/helpdesk && \
    chmod 666 /home/user/helpdesk/tickets.db && \
    chmod 755 /home/user

# Environment variables
ENV HELP_DESK_DIR=/home/user/helpdesk

WORKDIR /home/user/helpdesk

CMD ["/bin/bash"]