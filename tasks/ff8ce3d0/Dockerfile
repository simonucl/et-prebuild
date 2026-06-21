FROM ubuntu:22.04

# Help text from %help
# This container sets up the initial filesystem state for the localisation and
# mock-firewall task. It provides:
# * /home/user/firewall/active_rules.conf – six-line baseline policy
# * /home/user/localise-site/templates/messages.pot – template with 17-line header
# Pytest is pre-installed for automated validation.

ENV USER_HOME=/home/user
ENV FIREWALL_DIR=/home/user/firewall
ENV LOCALISE_DIR=/home/user/localise-site

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p "$FIREWALL_DIR" && \
    mkdir -p "$LOCALISE_DIR/templates"

RUN cat > "$FIREWALL_DIR/active_rules.conf" <<'EOF'
# Firewall Rules
# -----------------------------------------------------------------------------
# default policy : deny incoming, allow outgoing
# -----------------------------------------------------------------------------
# BEGIN RULES
# END RULES
EOF

RUN chmod 0666 "$FIREWALL_DIR/active_rules.conf"

RUN cat > "$LOCALISE_DIR/templates/messages.pot" <<'EOT'
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PROJECT VERSION\n"
"POT-Creation-Date: 2023-01-01 00:00+0000\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

#: placeholder:1
msgid "Hello, world!"
msgstr ""
EOT

RUN chmod -R 0777 "$LOCALISE_DIR" && \
    chmod 0777 "$FIREWALL_DIR" && \
    mkdir -p /home/user && \
    chmod 755 /home/user

LABEL Author="example-builder" \
      Description="Environment for localisation & user-level firewall exercise"