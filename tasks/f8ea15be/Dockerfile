FROM ubuntu:22.04

# Install Python tooling and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/string-service/config && \
    mkdir -p /home/user/string-service/logs

# Initial configuration
RUN echo 'LOCALE="en_US"' > /home/user/string-service/config/env.conf

# Empty log file
RUN : > /home/user/string-service/logs/translation_update.log

# Permissions
RUN chmod 777 /home/user/string-service /home/user/string-service/config /home/user/string-service/logs && \
    chmod 666 /home/user/string-service/config/env.conf /home/user/string-service/logs/translation_update.log

# From %environment (chmod must be RUN, no env vars present)
RUN chmod 755 /home/user