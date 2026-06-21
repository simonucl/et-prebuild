FROM ubuntu:22.04

# help text from %runscript
# Apptainer container ready for the Linux process-management exercise.
# Follow the assignment instructions inside this environment.

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/experiments && \
    chmod -R 0777 /home/user

RUN chmod 755 /home/user

CMD /bin/sh -c "echo 'Apptainer container ready for the Linux process-management exercise.' && echo 'Follow the assignment instructions inside this environment.'"