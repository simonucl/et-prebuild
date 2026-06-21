FROM ubuntu:22.04

# Help text from %help
# This image sets up the initial workspace for the localization
# transformation exercise. It pre-installs Python, pytest, and places the two
# required source CSV files under:
# /home/user/project/translations/

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates && \
    sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/project/translations

RUN cat <<'EOF' > /home/user/project/translations/en_US.csv
greeting,Hello
farewell,Goodbye
ask_name,What is your name?
thank_you,Thank you
welcome,Welcome
EOF

RUN cat <<'EOF' > /home/user/project/translations/es_ES.csv
greeting,Hola
farewell,Adiós
thank_you,Gracias
EOF

RUN chmod -R a+rwX /home/user/project

RUN chmod 755 /home/user

LABEL Author="ExampleAuthor"
LABEL Description="Base image for the localization transformation task"