FROM ubuntu:22.04

# Help text
# Container for encoding-migration task. Execute your commands as needed.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        file \
        locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/configs && \
    mkdir -p /home/user/change_logs && \
    chmod 0777 /home/user/configs && \
    chmod 0777 /home/user/change_logs

RUN python3 - << 'PYTHON_EOF'
import os, codecs, textwrap, stat

content = textwrap.dedent("""\
    # Sample Legacy Configuration
    database_host=localhost
    database_user=administrador
    welcome_message=Bem-vindo ao café!
    """)

os.makedirs("/home/user/configs", exist_ok=True)
with codecs.open("/home/user/configs/legacy.conf", "w", "latin-1") as fh:
    fh.write(content)

os.chmod("/home/user/configs/legacy.conf", 0o644)
PYTHON_EOF

RUN chmod 755 /home/user

CMD echo "Container for encoding-migration task. Execute your commands as needed."