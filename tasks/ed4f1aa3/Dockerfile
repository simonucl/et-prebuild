FROM ubuntu:22.04

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the initial documentation directory structure
RUN mkdir -p /home/user/projects/manual

# Create intro.md (31 bytes)
RUN cat > /home/user/projects/manual/intro.md <<'EOF'
## Intro
A brief introduction.
EOF

# Create install.md (31 bytes)
RUN cat > /home/user/projects/manual/install.md <<'EOF'
## Install
Use `make install`.
EOF

# Create usage.md (22 bytes)
RUN cat > /home/user/projects/manual/usage.md <<'EOF'
## Usage
Run `./app`.
EOF

# Ensure the files are readable by the unprivileged user
RUN chmod -R a+rX /home/user

# Set permissions on /home/user at runtime
RUN chmod 755 /home/user

# Labels
LABEL Author="Container setup for documentation-compression task"