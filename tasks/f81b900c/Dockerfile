FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/locale

RUN cat > /home/user/project/locale/ru.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: SAMPLE 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/main.c:10
msgid "File not found"
msgstr ""

#: src/main.c:20
msgid "Save changes?"
msgstr "Сохранить изменения?"

#: src/main.c:30
msgid "Are you sure you want to quit?"
msgstr ""

#: src/main.c:40
msgid "Preferences"
msgstr "Настройки"
EOF

RUN chmod -R 0777 /home/user/project

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD echo "Container for the localization diagnostics task."