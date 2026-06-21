FROM ubuntu:22.04

# Install required software: Python, pip, pytest, jq
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create project directory structure
RUN mkdir -p /home/user/project-localization/locales && \
    mkdir -p /home/user/project-localization/scripts && \
    mkdir -p /home/user/project-localization/dist

# .env.example
RUN cat > /home/user/project-localization/.env.example <<'EOF'
API_KEY=CHANGE_ME
DEFAULT_LOCALE=en_US
EOF

# locales/en_US.json
RUN cat > /home/user/project-localization/locales/en_US.json <<'EOF'
{
  "greeting": "Hello",
  "farewell": "Goodbye",
  "inquiry": "How are you?"
}
EOF

# locales/es_ES.json
RUN cat > /home/user/project-localization/locales/es_ES.json <<'EOF'
{
  "greeting": "Hola",
  "farewell": "Adiós",
  "inquiry": "¿Cómo estás?"
}
EOF

# build_translations.sh
RUN cat > /home/user/project-localization/scripts/build_translations.sh <<'EOF'
#!/usr/bin/env bash
set -e
if [ -z "$LOCALE" ]; then
  echo "LOCALE env variable not set" >&2
  exit 1
fi
mkdir -p dist
jq -r 'to_entries[] | "\(.key)=\(.value)"' "locales/${LOCALE}.json" > "dist/${LOCALE}.po"
echo "Built dist/${LOCALE}.po with $(wc -l < "dist/${LOCALE}.po") entries"
EOF

RUN chmod +x /home/user/project-localization/scripts/build_translations.sh

# Permissions
RUN chmod -R 0777 /home/user/project-localization && \
    chmod 755 /home/user

LABEL Author="localization_task_setup"
LABEL Description="Container initial state for French localisation exercise"

CMD echo "This container sets up the initial state for the localisation task." && \
    echo "Invoke your preferred shell to start working." && \
    /bin/bash