FROM ubuntu:22.04

# Author="GPT-4"
# Description="Container for db_ssl validation task with initial state and pytest installed."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN useradd -m -s /bin/bash user

RUN mkdir -p /home/user/sample_certs && \
    echo -n "test" > /home/user/sample_certs/ca.pem

RUN chown -R user:user /home/user && \
    chmod 755 /home/user /home/user/sample_certs && \
    chmod 644 /home/user/sample_certs/ca.pem

CMD ["bash"]