FROM ubuntu:22.04

# Labels
LABEL Author="DevOps-Apptainer-Setup"
LABEL Description="Base image with Python, pip and pytest installed. Provides writable /home/user for the student; leaves /home/user/logs absent as required by the assignment."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LANG=C
ENV TZ=UTC

CMD /bin/sh -c "echo 'Container built for timestamp-logging assignment.' && echo 'Python version: ' \$(python3 --version) && echo 'pytest version: ' \$(pytest --version | head -n 1)"