FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        locales && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/docs

# Create readme UTF-8 file
RUN cat > /tmp/readme_utf8.txt <<'EOF'
Curaçao project documentation
=============================
Version 1.0 - août 2023
...
EOF

# Create changelog UTF-8 file
RUN cat > /tmp/changelog_utf8.txt <<'EOF'
Changelog
---------
* 2023-08-15 : Première version publiée
* 2023-09-01 : Corrections mineures
EOF

# Create license UTF-8 file
RUN cat > /tmp/license_utf8.txt <<'EOF'
Licence MIT
------------
Copyright © 2023 ACME Corp.
Permission est accordée, gratuitement, à toute personne obtenant une copie...
EOF

# Convert files to ISO-8859-1 encoding and clean up
RUN for name in readme changelog license; do \
        iconv -f UTF-8 -t ISO-8859-1 /tmp/${name}_utf8.txt -o /home/user/project/docs/${name}.txt; \
    done && \
    rm /tmp/*_utf8.txt && \
    chmod -R 755 /home/user && \
    find /home/user -type f -exec chmod 644 {} \; && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8