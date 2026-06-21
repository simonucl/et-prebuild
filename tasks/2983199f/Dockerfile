FROM ubuntu:22.04

# From %post
RUN set -e && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-client python3 python3-pip && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir pytest
RUN mkdir -p /home/user && chmod 0777 /home/user

# From %environment
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# From %help and %runscript
# Container ready. Execute your commands inside the shell.