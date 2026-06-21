FROM ubuntu:22.04

# Labels
LABEL Author="task-preparer"
LABEL Description="Environment for site administrator task – initial state only."

# Post installation
RUN set -e && \
    echo "Updating apt and installing python3-pip..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure expected by the tests
RUN BASE=/home/user && \
    SITE_ADMIN=${BASE}/site_admin && \
    WWW=${SITE_ADMIN}/www && \
    echo "Creating site_admin directory tree..." && \
    mkdir -p "${WWW}/alice" "${WWW}/bob" "${WWW}/charlie"

# Create users.csv with exact required initial contents (4 lines, trailing newline)
RUN cat > /home/user/site_admin/users.csv <<'EOF'
username,status
alice,active
bob,active
charlie,active
EOF

# Create minimal index.html files for existing users
RUN echo "<h1>Welcome, alice!</h1>" > /home/user/site_admin/www/alice/index.html && \
    echo "<h1>Welcome, bob!</h1>" > /home/user/site_admin/www/bob/index.html && \
    echo "<h1>Welcome, charlie!</h1>" > /home/user/site_admin/www/charlie/index.html

# Make everything writable by non-root users who will run inside the container
RUN chmod -R 777 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD echo "Container for site administrator task." && echo "No default runtime action – please run your solution script or open a shell."