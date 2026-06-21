FROM ubuntu:22.04

# Install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install pytest && \
    rm -rf /var/lib/apt/lists/*

# Create /home/user and ensure it is writable by the non-root runtime user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create the data directory and JSON file with the required permissions
RUN mkdir -p /home/user/data && \
    chmod 0755 /home/user/data

RUN cat >/home/user/data/release_config.json <<'EOF'
[
  { "service": "auth",    "version": "v1.2.0", "port": 8000 },
  { "service": "billing", "version": "1.0.0",  "port": 8010 },
  { "service": "search",  "version": "v2.0.1", "port": 8020 },
  { "service": "legacy",  "version": "v3.0",   "port": 8030 },
  { "service": "reports", "version": "v4.1.0", "port": 8040 }
]
EOF

RUN chmod 0644 /home/user/data/release_config.json

# NOTE: /home/user/logs and the output file must NOT exist initially,
# so they are intentionally not created here.

ENV LC_ALL=C
ENV LANG=C

# Labels
LABEL Author="ChatGPT"
LABEL Description="Container for semantic version smoke-test assignment with jq and pytest pre-installed."

WORKDIR /home/user