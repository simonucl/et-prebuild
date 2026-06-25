FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    coreutils \
    findutils \
    gzip \
    jq \
    nodejs \
    npm \
    python3 \
    tar \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

COPY rootfs/ /
RUN chown -R user:user /home/user

WORKDIR /home/user
