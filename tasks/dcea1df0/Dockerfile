FROM ubuntu:22.04

# Install system packages needed for Python work
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the validation test-suite
RUN pip3 install --no-cache-dir pytest

# Create the initial project tree expected by the automated checker
RUN mkdir -p \
    /home/user/project/locale/templates \
    /home/user/project/locale/en_US/LC_MESSAGES \
    /home/user/project/locale/fr_FR/LC_MESSAGES

# Template .pot file
RUN cat > /home/user/project/locale/templates/app.pot <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: app 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/main.py:10
msgid "HELLO_WORLD"
msgstr "Hello, World!"

#: src/main.py:20
msgid "MSG_NEW"
msgstr "A new message"
EOF

# English .po file (HELLO_WORLD only)
RUN cat > /home/user/project/locale/en_US/LC_MESSAGES/app.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: app 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/main.py:10
msgid "HELLO_WORLD"
msgstr "Hello, World!"
EOF

# French .po file (HELLO_WORLD only)
RUN cat > /home/user/project/locale/fr_FR/LC_MESSAGES/app.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: app 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/main.py:10
msgid "HELLO_WORLD"
msgstr "Bonjour, Monde!"
EOF

# Make sure every participant can read/write the project directory
RUN chmod -R a+rwx /home/user || true

# Create symlink for python command
RUN if [ -x /usr/bin/python3 ] && [ ! -e /usr/bin/python ]; then \
        ln -sf /usr/bin/python3 /usr/local/bin/python; \
    fi

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Set working directory
WORKDIR /home/user