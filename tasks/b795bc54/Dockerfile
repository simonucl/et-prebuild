# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / metadata
LABEL Author="localization_setup"
LABEL Description="Environment for localization engineer task with pytest pre-installed."

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gettext \
        procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project_i18n

RUN cat > /home/user/project_i18n/messages.pot <<'POT'
msgid ""
msgstr ""
"Project-Id-Version: example 1.0\n"
"Language: en\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/main.c:10
msgid "Hello, world!"
msgstr ""

#: src/main.c:20
msgid "Goodbye."
msgstr ""
POT

RUN cat > /home/user/project_i18n/fr.po <<'PO'
msgid ""
msgstr ""
"Project-Id-Version: example 1.0\n"
"Language: fr\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/main.c:10
msgid "Hello, world!"
msgstr "Bonjour le monde!"
PO

RUN chmod 644 /home/user/project_i18n/messages.pot && \
    chmod 644 /home/user/project_i18n/fr.po && \
    chmod 755 /home/user && \
    chmod 755 /home/user/project_i18n