FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Container for the SQL refactoring task with pytest pre-installed."

# Set environment variables
ENV PYTHONIOENCODING="utf-8"
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV DEBIAN_FRONTEND=noninteractive

# Basic tooling
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare directory structure
RUN mkdir -p /home/user/db/queries/daily && \
    mkdir -p /home/user/db/queries/archive && \
    mkdir -p /home/user/db/queries/maintenance && \
    mkdir -p /home/user/db/optimization

# Create daily/report.sql (recent file)
RUN cat <<'EOF' > /home/user/db/queries/daily/report.sql
/* daily report */
SELECT * FROM sales;
LIMIT 100;
EOF

# Create archive/old_report.sql (older file)
RUN cat <<'EOF' > /home/user/db/queries/archive/old_report.sql
/* archived report */
SELECT * FROM sales;
EOF

# Create maintenance/cleanup.sql (older file)
RUN cat <<'EOF' > /home/user/db/queries/maintenance/cleanup.sql
/* maintenance task */
DELETE FROM logs WHERE date < NOW() - INTERVAL '30 days';
EOF

# Set permissions so an unprivileged agent can modify the tree
RUN chmod -R a+rwX /home/user/db

# Adjust timestamps:
#   * daily/report.sql     → within last 7 days
#   * others               → older than 7 days
RUN touch -d "2 days ago"  /home/user/db/queries/daily/report.sql && \
    touch -d "10 days ago" /home/user/db/queries/archive/old_report.sql && \
    touch -d "10 days ago" /home/user/db/queries/maintenance/cleanup.sql

# Set home directory permissions
RUN chmod 755 /home/user