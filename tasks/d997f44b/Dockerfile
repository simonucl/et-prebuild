FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem expected by the assignment
# Home directory for the learner
RUN mkdir -p /home/user

# Microservice directories and version files (no trailing newlines)
RUN mkdir -p /home/user/microservices/service-alpha && \
    mkdir -p /home/user/microservices/service-beta

RUN printf '1.0.0' > /home/user/microservices/service-alpha/version.txt && \
    printf '2.1.3' > /home/user/microservices/service-beta/version.txt

# Ensure non-root users have read access
RUN chmod -R a+rX /home/user/microservices && \
    chmod a+rx /home/user && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8