FROM ubuntu:22.04

# Author: csv-localization-task
# Description: Container with initial dataset for column-reordering exercise

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    pip3 install --no-cache-dir pytest && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    mkdir -p /home/user/project/translations

RUN cat > /home/user/project/translations/messages.csv <<'EOF'
key,en,de,fr,es,it
greeting,Hello,Hallo,Bonjour,Hola,Ciao
farewell,Goodbye,Auf Wiedersehen,Au revoir,Adiós,Arrivederci
thank_you,Thank you,Danke,Merci,Gracias,Grazie
yes,Yes,Ja,Oui,Sí,Sì
no,No,Nein,Non,No,Nessuno
please,Please,Bitte,S'il vous plaît,Por favor,Per favore
sorry,Sorry,Entschuldigung,Désolé,Lo siento,Mi dispiace
welcome,Welcome,Willkommen,Bienvenue,Bienvenido,Benvenuto
congrats,Congratulations,Herzlichen Glückwunsch,Félicitations,Felicitaciones,Congratulazioni
morning,Good morning,Guten Morgen,Bonjour,Buenos días,Buongiorno
EOF

RUN chmod 644 /home/user/project/translations/messages.csv && \
    rm -f /home/user/project/translations/updated_messages.csv \
          /home/user/project/translations/update_log.txt || true && \
    chmod 755 /home/user

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

CMD echo "Container ready. Execute your shell commands to complete the task."