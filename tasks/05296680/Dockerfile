FROM ubuntu:22.04

# Help/labels
LABEL Author="Exoplanet-Setup"
LABEL Description="Environment for exoplanet re-organisation exercise. Contains initial CSV dataset and empty output directory. Pytest pre-installed."

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    chmod 755 /home/user && \
    chown 1000:1000 /home/user || true

RUN mkdir -p /home/user/data && \
    chmod 755 /home/user/data

RUN cat <<'CSV_EOF' > /home/user/data/exoplanets.csv
pl_name,hostname,disc_year,discoverymethod,pl_orbper
"Kepler-22 b","Kepler-22",2011,Transit,289.8623
"HD 209458 b","HD 209458",1999,Transit,3.5247
"51 Pegasi b","51 Pegasi",1995,Radial Velocity,4.2308
"Kepler-10 c","Kepler-10",2011,Transit,45.2943
"GJ 1214 b","GJ 1214",2009,Transit,1.5804
CSV_EOF

RUN chmod 644 /home/user/data/exoplanets.csv && \
    chown 1000:1000 /home/user/data/exoplanets.csv || true

RUN mkdir -p /home/user/output && \
    chmod 755 /home/user/output && \
    chown 1000:1000 /home/user/output || true