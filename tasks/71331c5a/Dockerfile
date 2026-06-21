FROM ubuntu:22.04

# Author: localization-task-setup
# Description: "Initial environment for localisation compilation exercise"

# ------------------------------------------------------------------ #
# Basic tooling and Python test dependencies                         #
# ------------------------------------------------------------------ #
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        gettext && \
    python3 -m pip install --no-cache-dir pytest

# ------------------------------------------------------------------ #
# Create directory skeleton                                           #
# ------------------------------------------------------------------ #
RUN install -d -m 755 /home/user && \
    install -d -m 755 /home/user/localization/source && \
    install -d -m 755 /home/user/localization/project/po && \
    install -d -m 777 /home/user/localization/logs

# ------------------------------------------------------------------ #
# Populate template POT file                                          #
# ------------------------------------------------------------------ #
RUN cat > /home/user/localization/source/messages.pot <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: Demo 1.1\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

#: hello.c:10
msgid "Hello"
msgstr ""

#: bye.c:11
msgid "Good-bye"
msgstr ""
EOF

RUN touch -d "@1700000000" /home/user/localization/source/messages.pot && \
    chmod 644 /home/user/localization/source/messages.pot

# ------------------------------------------------------------------ #
# Populate initial PO files                                           #
# ------------------------------------------------------------------ #
RUN cat > /home/user/localization/project/po/en.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: Demo 1.0\n"
"Language: en\n"

#: hello.c:10
msgid "Hello"
msgstr "Hello"
EOF

RUN cat > /home/user/localization/project/po/fr.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: Demo 1.0\n"
"Language: fr\n"

#: hello.c:10
msgid "Hello"
msgstr "Bonjour"
EOF

RUN cat > /home/user/localization/project/po/es.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: Demo 1.0\n"
"Language: es\n"

#: hello.c:10
msgid "Hello"
msgstr "Hola"
EOF

# Make PO files world-writable so the non-root runtime user can update them
RUN chmod 666 /home/user/localization/project/po/*.po

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

CMD ["echo", "Docker image prepared for localisation task. Execute your build script inside the container."]