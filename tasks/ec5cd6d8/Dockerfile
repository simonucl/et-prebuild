# Author: TranslationTaskSetup
# Description: Environment for translation report scripting task with pytest pre-installed.
# Run script note: Container for translation report task. Run your commands within an interactive shell.

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project/i18n

RUN cat > /home/user/project/i18n/template.pot <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: Sample Project\n"
"Pot-Creation-Date: 2022-10-10 12:00+0000\n"
"Language: \n"

#: src/ui.c:10
msgid "Hello"
msgstr ""

#: src/ui.c:20
msgid "Goodbye"
msgstr ""

#: src/ui.c:30
msgid "Cancel"
msgstr ""
EOF

RUN cat > /home/user/project/i18n/fr.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: Sample Project\n"
"Language: fr\n"

#: src/ui.c:10
msgid "Hello"
msgstr "Bonjour"

#: src/ui.c:20
msgid "Goodbye"
msgstr ""

#: src/ui.c:30
msgid "Cancel"
msgstr ""
EOF

RUN cat > /home/user/project/i18n/es.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: Sample Project\n"
"Language: es\n"

#: src/ui.c:10
msgid "Hello"
msgstr "Hola"

#: src/ui.c:20
msgid "Goodbye"
msgstr "Adiós"

#: src/ui.c:30
msgid "Cancel"
msgstr ""
EOF

RUN chmod 755 /home/user && chmod 644 /home/user/project/i18n/*.po && chmod 644 /home/user/project/i18n/template.pot

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"