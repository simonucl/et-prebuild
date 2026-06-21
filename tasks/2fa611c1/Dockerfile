# Converted from Apptainer definition
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial project structure
RUN mkdir -p /home/user/project/i18n

RUN cat > /home/user/project/i18n/messages.po <<'EOF'
# SOME DESCRIPTIVE TITLE.
msgid ""
msgstr ""
"Project-Id-Version: PROJECT VERSION\n"
"Language: es_ES\n"

#: src/main.c:10
msgid "File"
msgstr ""

#: src/main.c:11
msgid "Edit"
msgstr ""

#: src/main.c:12
msgid "View"
msgstr "Vista"

#: src/main.c:13
msgid "Help"
msgstr ""
EOF

# Permissions
RUN chmod -R 777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Label
LABEL Author="localization-task-setup"