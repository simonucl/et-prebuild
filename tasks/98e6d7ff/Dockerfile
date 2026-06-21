FROM ubuntu:22.04

# Update base system and install Python tooling
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state expected by the automated tests
RUN mkdir -p /home/user/docs && \
    chmod 0777 /home/user/docs

# Create the required CSV file with exact contents
RUN cat <<'EOF' > /home/user/docs/index.csv
id,title,section
1,Introduction,Getting Started
2,Installation,Getting Started
3,Configuration,Advanced Topics
4,FAQ,Appendix
EOF

RUN chmod 0644 /home/user/docs/index.csv

# Clean up apt caches to keep the image lean
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Permissions from %environment
RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8