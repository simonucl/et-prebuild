# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# --------------------------------------------------
# Base tools + Python test framework
# --------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Prepare initial project tree and localisation files
# --------------------------------------------------
RUN mkdir -p /home/user/project/locale

# Master English INI
RUN cat <<"EOF_EN" > /home/user/project/locale/en_US.ini
[CORE]
greeting = Hello
farewell = Goodbye
prompt   = What would you like to do?
thanks   = Thank you
error_message = An unexpected error has occurred.
EOF_EN

# French translation INI (missing two new keys)
RUN cat <<"EOF_FR" > /home/user/project/locale/fr_FR.ini
[CORE]
greeting = Bonjour
farewell = Au revoir
prompt   = Que voulez-vous faire ?
EOF_FR

# Ensure there is exactly one trailing newline
RUN echo >> /home/user/project/locale/fr_FR.ini

# Make everything under /home/user writable
RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

# --------------------------------------------------
# Environment configuration
# --------------------------------------------------
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# --------------------------------------------------
# Help / runscript equivalent
# --------------------------------------------------
# Container for localisation sync task.
# Run your commands inside an interactive shell or via 'docker exec'.