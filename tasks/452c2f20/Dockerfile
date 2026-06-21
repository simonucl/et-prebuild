FROM ubuntu:22.04

# Help / labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for localisation engineering exercise with pytest pre-installed."

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project-l18n/translations

RUN cat > /home/user/project-l18n/.env <<'EOF'
API_URL=https://api.example.com
FEATURE_X=true
MAX_RETRIES=5
EOF

RUN printf '{"hello":"Hello","bye":"Good-bye"}\n' \
    > /home/user/project-l18n/translations/messages.en.json

RUN printf '{"hello":"Hola","bye":"Adiós"}\n' \
    > /home/user/project-l18n/translations/messages.es.json

RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

ENV PATH="$PATH:/usr/local/bin"