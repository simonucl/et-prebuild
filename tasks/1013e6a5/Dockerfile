FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial directory structure and template file
RUN mkdir -p /home/user/templates/optimization

RUN cat > /home/user/templates/optimization/solver_template.conf <<'EOF'
# Solver Configuration Template
algorithm=template
learning_rate=0.01
max_iterations=200
tolerance=1e-6
EOF

# Ensure the student can write inside /home/user
RUN chmod -R a+rwX /home/user

# Clean up APT cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment settings
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="task-preparer"