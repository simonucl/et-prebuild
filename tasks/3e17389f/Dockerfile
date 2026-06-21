FROM ubuntu:22.04

# Base tools and Python environment
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/db_queries && \
    chmod -R 0777 /home/user

RUN cat > /home/user/db_queries/raw_queries.sql <<'EOF'
SELECT * from employees where salary>50000;
select name, department from employees where department='Sales';
EOF

RUN chmod 0666 /home/user/db_queries/raw_queries.sql

# Environment settings
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN chmod 755 /home/user

# Labels
LABEL Author="SQL optimisation task base image"