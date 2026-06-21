FROM ubuntu:22.04

# Author localization-engineer
# Description "Container for translation-update task; includes initial project skeleton and pytest."

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-venv && \
    pip3 install --no-cache-dir --upgrade pip pytest && \
    groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user || true && \
    install -d -m 0755 /home/user && \
    install -d -m 0755 /home/user/project/locale/fr/LC_MESSAGES

RUN cat <<'EOF' > /home/user/project/locale/fr/LC_MESSAGES/messages.po
# French translations – OLD
msgid "Hello"
msgstr "Bonjour (old)"
msgid "Bye"
msgstr "Au revoir (old)"
EOF

RUN install -d -m 0755 /home/user/updates

RUN cat <<'EOF' > /home/user/updates/fr.po
# French translations – NEW
msgid "Hello"
msgstr "Bonjour"
msgid "Bye"
msgstr "Au revoir"
EOF

RUN install -d -m 0755 /home/user/update_logs && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user