# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: localization-task-builder
# Description: Container for the French localization update task.

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN mkdir -p /home/user/project/localization

RUN cat > /home/user/project/localization/translations_master.tsv << 'EOF'
key	en_US	fr_FR	es_ES
greeting	Hello	Bonjour	Hola
farewell	Goodbye	Au revoir	Adiós
thanks	Thank you	Merci	Gracias
yes	Yes	Oui	Sí
no	No	Non	No
EOF

RUN cat > /home/user/project/localization/fr_updates.tsv << 'EOF'
fr_FR
Salut
Au revoir
Merci
Oui
Non
EOF

RUN chmod 0777 /home/user/project/localization && \
    chmod 0666 /home/user/project/localization/*.tsv

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user