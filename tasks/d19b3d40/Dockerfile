FROM ubuntu:22.04

# Author user
# Description "Environment for log-archiving exercise with pytest pre-installed."

# This container sets up the initial state for the
# log-archiving exercise and includes PyTest for automated grading.

RUN set -e && \
    echo "Updating apt repositories and installing Python/pip..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates gcc make \
        > /dev/null && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating unprivileged user 'user' (uid 1000) ..." && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

RUN echo "Setting up initial directory /home/user/sample_logs ..." && \
    su - user -c '\
        mkdir -p /home/user/sample_logs && \
        cd /home/user/sample_logs && \
        for fname in log1.log log2.log log3.log; do \
            dd if=/dev/zero of="$fname" bs=1 count=0 seek=1048576 2>/dev/null; \
        done \
    '

# Ensure the archive directory does NOT exist in the initial state
RUN rm -rf /home/user/archive

RUN echo "Initial environment prepared."

# Environment setup
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

WORKDIR /home/user

CMD ["/bin/bash"]