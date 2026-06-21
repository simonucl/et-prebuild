FROM ubuntu:22.04

# Help:
# This container provides:
#   • Python (accessible via `python`) with the built-in http.server module
#   • pytest (used by the autograder)
#   • An initial dataset directory at /home/user/datasets containing sales.csv
# Students will create a throw-away web-server and log-file as per the task instructions.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python-is-python3 \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/datasets && \
    chmod 755 /home/user /home/user/datasets

RUN cat >/home/user/datasets/sales.csv <<'EOF'
date,region,sales
2023-01-01,North,100
2023-01-02,South,150
EOF

RUN chmod 644 /home/user/datasets/sales.csv

CMD ["/bin/bash"]