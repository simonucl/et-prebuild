# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# Container for the name-frequency cleaning exercise.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/datasets

RUN cat > /home/user/datasets/raw_names.txt <<'EOF'
Alice
bob
Charlie
alice
Bob
alice   
Alice
charlie
Bob
Dana
Eve
eve
Eve
alice
bob
dana
Eve
Alice
charlie
EOF

RUN chmod -R a+rX /home/user && \
    chmod -R u+w,g+w,o+w /home/user && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD /bin/sh -c "echo 'Container for the name-frequency cleaning exercise.' && echo 'You are now inside the container. Good luck!'"