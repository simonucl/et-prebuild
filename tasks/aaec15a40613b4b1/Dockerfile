FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && \
    apt-get install -y --no-install-recommends bash ca-certificates coreutils findutils openjdk-21-jdk-headless python3 unzip zip && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

COPY rootfs/ /
RUN chown -R user:user /home/user/jar_lab

USER user
WORKDIR /home/user
