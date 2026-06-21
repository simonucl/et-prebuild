FROM ubuntu:22.04

# Help section not provided, so none added

RUN set -e && apt-get update -y && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    rsync \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user
RUN mkdir -p /home/user/project/public

RUN printf '<html>Index</html>\n' > /home/user/project/index.html
RUN printf 'top secret\n' > /home/user/project/secret.txt
RUN printf 'Project read-me\n' > /home/user/project/readme.md
RUN printf 'DB_PASS=1234\n' > /home/user/project/.env

RUN printf 'body {margin:0;}\n' > /home/user/project/public/style.css
RUN printf '#!/bin/bash\necho hi\n' > /home/user/project/public/script.sh

RUN chmod 0644 /home/user/project/index.html && \
    chmod 0600 /home/user/project/secret.txt && \
    chmod 0664 /home/user/project/readme.md && \
    chmod 0600 /home/user/project/.env && \
    chmod 0644 /home/user/project/public/style.css && \
    chmod 0755 /home/user/project/public/script.sh

RUN mkdir -p /home/user/simulated_remote && chmod 0777 /home/user/simulated_remote

RUN chown -R 0:0 /home/user

RUN chmod 755 /home/user

ENV PATH=/usr/bin:$PATH