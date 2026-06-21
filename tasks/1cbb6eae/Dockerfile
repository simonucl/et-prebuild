FROM ubuntu:22.04

# Help/comment section
# Container providing the initial state for the credential-rotation drill

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/credentials

RUN cat > /home/user/credentials/old_credentials.txt <<'EOF'
serviceA,pass1234
serviceB,mysecret
serviceC,qwerty
EOF

RUN chmod 0777 /home && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/credentials && \
    chmod 0666 /home/user/credentials/old_credentials.txt && \
    chmod 755 /home/user

LABEL Author="Apptainer automation" \
      Description="Container providing the initial state for the credential-rotation drill"

CMD sh -c 'echo "Container for credential-rotation drill. Execute your tasks in an interactive shell."; exec /bin/bash --noprofile --norc "$@"'