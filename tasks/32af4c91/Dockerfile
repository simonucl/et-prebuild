FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        file \
        locales \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8

# Python testing framework
RUN pip3 install --no-cache-dir pytest

# Create project structure
RUN mkdir -p /home/user/mobile_pipeline/i18n_source && \
    chmod 0755 /home && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/mobile_pipeline && \
    chmod 0755 /home/user/mobile_pipeline/i18n_source

# en_US.properties
RUN printf "greeting=Hello\r\nfarewell=Goodbye\r\ncurrency=Dollar\r\n" > /home/user/mobile_pipeline/i18n_source/en_US.properties

# es_ES.properties
RUN printf "greeting=Hola\r\nfarewell=Adiós\r\ncurrency=Euro\r\n" > /home/user/mobile_pipeline/i18n_source/es_ES.properties

# jp_JP.properties
RUN printf "greeting=??????\r\nfarewell=??????\r\ncurrency=??\r\n" > /home/user/mobile_pipeline/i18n_source/jp_JP.properties

# Set permissions on properties files
RUN chmod 0644 /home/user/mobile_pipeline/i18n_source/*.properties

# README.txt
RUN cat << 'EOF' > /home/user/mobile_pipeline/README.txt
This pipeline contains localisation resources.
Do not edit files in i18n_source/ manually.
EOF
RUN chmod 0644 /home/user/mobile_pipeline/README.txt

# Environment
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en

# Help text (from runscript)
# Container for the i18n transcoding exercise.
# Run your commands inside the container shell.