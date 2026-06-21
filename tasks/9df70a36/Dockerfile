FROM ubuntu:22.04

# Help section was empty in original

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/bin && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/bin

RUN chmod 755 /home/user

ENV PATH=/home/user/bin:$PATH