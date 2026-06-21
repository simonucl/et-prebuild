FROM ubuntu:22.04

# From %post
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    mkdir -p /home/user/localization && \
    chmod 0755 /home/user/localization

RUN cat > /home/user/localization/translations.csv <<'CSV'
key,en_US,fr_FR,de_DE
welcome,Welcome,,Willkommen
bye,Goodbye,Au revoir,Auf Wiedersehen
thanks,Thank you,,Danke
hello,Hello,Bonjour,Hallo
morning,Good morning,,Guten Morgen
CSV

RUN chmod 0644 /home/user/localization/translations.csv && \
    chown -R 1000:1000 /home/user

# From %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

# From %runscript
# Apptainer image for the 'missing French translations' exercise.
# Invoke commands inside the container with 'apptainer exec'.