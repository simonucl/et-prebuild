FROM ubuntu:22.04

# Help section omitted (not provided)

ENV PATH="/home/user/.local/bin:$PATH"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        coreutils \
        grep \
        dpkg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

RUN if ! grep -q "^user:" /etc/passwd; then \
        echo "user:x:1001:1001:User,,,:/home/user:/bin/bash" >> /etc/passwd; \
    fi

RUN chmod 755 /home/user

CMD ["bash", "-l"]