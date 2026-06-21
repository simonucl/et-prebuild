FROM ubuntu:22.04

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create required directory structure
RUN mkdir -p /home/user/pg_sandbox

# Populate postgresql.conf
RUN cat > /home/user/pg_sandbox/postgresql.conf <<'EOF'
#------------------------------------------------------------------------------
# ERROR REPORTING AND LOGGING
#------------------------------------------------------------------------------
#log_min_duration_statement = -1        # -1 disables, 0 logs all statements
#log_line_prefix = '%t [%p]: '          # see "logging parameters" in docs

#------------------------------------------------------------------------------
# CUSTOM PARAMETERS
#------------------------------------------------------------------------------
# (other parameters may follow)
EOF

# Ensure proper permissions
RUN chmod 755 /home/user && \
    chmod -R 777 /home/user/pg_sandbox

ENV PATH="/usr/bin:${PATH}"
ENV PYTHONIOENCODING="utf-8"

CMD ["bash"]