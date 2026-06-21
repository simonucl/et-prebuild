FROM ubuntu:22.04

# Help / metadata
LABEL Author="example"
LABEL Description="Container for IoT firewall rule preparation exercise – includes Python and pytest only."

# Post section
RUN set -eux && \
    useradd -m -s /bin/bash user

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Environment section
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["/bin/bash"]