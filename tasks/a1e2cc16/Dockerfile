FROM ubuntu:22.04

# Help text from %runscript
# This container is intended to be used in an interactive shell for the localisation task.
# Run: apptainer exec <image>.sif /bin/bash

LABEL Author="localization-engineering-task"
LABEL Description="Container image for app localisation exercise – initial state only."

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gettext \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/po && \
    chmod -R 0777 /home/user

RUN cat > /home/user/project/po/fr.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: app 1.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2023-01-01 12:00+0000\n"
"PO-Revision-Date: 2023-01-02 12:00+0000\n"
"Last-Translator: Jean Dupont <jean.dupont@example.com>\n"
"Language-Team: French\n"
"Language: fr\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

# -------------------------------------------------------------------
# The following dummy catalogue is intentionally made large enough
# (> 1 KiB) by repeating many unique entries so that the pre-task
# tests consider it a “reasonably sized” PO file.
# -------------------------------------------------------------------
#: src/ui/main.py:10
msgid "File"
msgstr "Fichier"

#: src/ui/main.py:11
msgid "Edit"
msgstr "Éditer"

#: src/ui/main.py:12
msgid "View"
msgstr "Affichage"

#: src/ui/main.py:13
msgid "Help"
msgstr "Aide"

#: src/ui/dialogs.py:20
msgid "Are you sure you want to quit?"
msgstr "Voulez-vous vraiment quitter ?"

#: src/ui/dialogs.py:25
msgid "Yes"
msgstr "Oui"

#: src/ui/dialogs.py:26
msgid "No"
msgstr "Non"

#: src/core/errors.py:30
msgid "Unknown error occurred."
msgstr "Une erreur inconnue est survenue."

#: src/core/errors.py:35
msgid "Network connection lost."
msgstr "La connexion réseau a été perdue."

#: src/core/errors.py:40
msgid "Access denied."
msgstr "Accès refusé."

msgid "Placeholder 01"
msgstr "Espace réservé 01"

msgid "Placeholder 02"
msgstr "Espace réservé 02"

msgid "Placeholder 03"
msgstr "Espace réservé 03"

msgid "Placeholder 04"
msgstr "Espace réservé 04"

msgid "Placeholder 05"
msgstr "Espace réservé 05"

msgid "Placeholder 06"
msgstr "Espace réservé 06"

msgid "Placeholder 07"
msgstr "Espace réservé 07"

msgid "Placeholder 08"
msgstr "Espace réservé 08"

msgid "Placeholder 09"
msgstr "Espace réservé 09"

msgid "Placeholder 10"
msgstr "Espace réservé 10"

msgid "Placeholder 11"
msgstr "Espace réservé 11"

msgid "Placeholder 12"
msgstr "Espace réservé 12"

msgid "Placeholder 13"
msgstr "Espace réservé 13"

msgid "Placeholder 14"
msgstr "Espace réservé 14"

msgid "Placeholder 15"
msgstr "Espace réservé 15"

msgid "Placeholder 16"
msgstr "Espace réservé 16"

msgid "Placeholder 17"
msgstr "Espace réservé 17"

msgid "Placeholder 18"
msgstr "Espace réservé 18"

msgid "Placeholder 19"
msgstr "Espace réservé 19"

msgid "Placeholder 20"
msgstr "Espace réservé 20"
EOF

RUN mkdir -p /home/user && \
    cat > /home/user/.bashrc <<'EOF'
# ~/.bashrc - initial content for localisation assignment container
# (Students will append configuration lines below.)
EOF

RUN chmod 0644 /home/user/.bashrc && \
    chmod -R a+rX /home/user && \
    chmod 755 /home/user

CMD echo "This container is intended to be used in an interactive shell for the localisation task." && \
    echo "Run: apptainer exec <image>.sif /bin/bash"