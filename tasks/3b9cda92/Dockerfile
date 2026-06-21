FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user

RUN cat >/home/user/images_to_migrate.log <<'EOF'
nginx:1.19
redis:6
nginx:1.19
mongo:4.4
nginx:1.19
redis:6
postgres:12
mongo:4.4
redis:6
redis:6
postgres:12
EOF

RUN chmod 777 /home/user && \
    chmod 666 /home/user/images_to_migrate.log

ENV PYTHONIOENCODING=UTF-8
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN chmod 755 /home/user

# Container for the 'Generate an image-frequency report with sort & uniq' task.
# Open a shell inside the container to begin working:
#     apptainer exec <image>.sif /bin/bash