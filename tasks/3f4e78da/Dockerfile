FROM ubuntu:22.04

# %post
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/docs/meta

RUN cat >/home/user/docs/meta/part1.csv <<'EOF'
doc_id,title,topic
101,Installation Guide,Setup
102,User Manual,Usage
103,Troubleshooting,Troubleshooting
105,API Reference,API
EOF

RUN cat >/home/user/docs/meta/part2.csv <<'EOF'
doc_id,title,topic
102,User Manual,Usage
104,Release Notes,Release
106,FAQ,Support
101,Installation Guide,Setup
EOF

RUN chmod 0644 /home/user/docs/meta/part1.csv /home/user/docs/meta/part2.csv && \
    chmod -R a+rx /home/user

# %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# %labels
LABEL Author="technical-writer-setup"
LABEL Description="Container with initial state for documentation consolidation task"

# %help
# This Apptainer image contains the prerequisite CSV files under
# /home/user/docs/meta/ and has pytest pre-installed for automated grading.