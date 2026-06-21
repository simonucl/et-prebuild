FROM ubuntu:22.04

# Author example@example.com
# Description "Container for the certificate-migration task: provides initial filesystem state and tooling."
# This image contains the starting environment for the certificate-migration exercise.
# All necessary tools (openssl, pytest, etc.) are installed and the filesystem layout matches the task description.

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip openssl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/microservices/gateway && \
    mkdir -p /home/user/microservices/certs

RUN cat <<'EOF' > /home/user/microservices/gateway/config.yaml
ssl:
  cert: ../certs/old_cert.pem
  key : ../certs/old_key.pem
mode: production
EOF

RUN echo 'dummy' > /home/user/microservices/certs/old_cert.pem && \
    echo 'dummy' > /home/user/microservices/certs/old_key.pem

RUN chmod -R a+rwX /home/user

# Equivalent of %runscript behavior
RUN chmod 755 /home/user

CMD echo "This container is prepared for the certificate-migration task." && \
    echo "Invoke your preferred shell to begin." && \
    /bin/bash