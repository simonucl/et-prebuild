FROM ubuntu:22.04

# Help section was not provided; none added.

RUN set -e && \
    echo "Installing Python and pytest ..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    echo "Preparing initial dataset ..." && \
    mkdir -p /home/user/raw_runs && \
    chmod 0777 /home/user && \
    chmod 0755 /home/user/raw_runs

RUN cat > /home/user/raw_runs/app_alpha.run <<'EOF'
tick 1
tick 2
tick 3
tick 4
tick 5
tick 6
tick 7
tick 8
tick 9
tick 10
tick 11
tick 12
tick 13
tick 14
tick 15
EOF

RUN cat > /home/user/raw_runs/app_beta.run <<'EOF'
tick 1
tick 2
tick 3
tick 4
tick 5
tick 6
tick 7
tick 8
tick 9
tick 10
tick 11
tick 12
tick 13
tick 14
tick 15
tick 16
tick 17
tick 18
tick 19
tick 20
tick 21
tick 22
EOF

RUN cat > /home/user/raw_runs/app_gamma.run <<'EOF'
tick 1
tick 2
tick 3
tick 4
tick 5
tick 6
tick 7
tick 8
tick 9
EOF

RUN chmod 0644 /home/user/raw_runs/*.run

RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8