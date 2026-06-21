FROM ubuntu:22.04

# Author      "Container build script for encoding exercise"
# Description "Provides initial state with three Latin-1 text files for students"
# Version     "1.0"

# This container delivers the starting environment for the
# "encoding conversion" exercise.  It pre-installs pytest for
# automated grading and populates
#   /home/user/support/incoming/
# with the required ISO-8859-1 encoded files.

#-----------------------------------------------------------------
# 1. Base packages and Python tooling
#-----------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        file \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

#-----------------------------------------------------------------
# 2. Prepare initial exercise data
#    /home/user/support/incoming/  with three Latin-1 files
#-----------------------------------------------------------------
RUN mkdir -p /home/user/support/incoming && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/support

# Create UTF-8 source texts
RUN tmpdir="$(mktemp -d)" && \
    cat > "${tmpdir}/clients_es.utf8" <<'EOF'
ID,Nombre,País
1,Ana,Costa Rica
2,José,México
3,María,España
EOF

RUN tmpdir="$(mktemp -d)" && \
    cat > "${tmpdir}/résumé_fr.utf8" <<'EOF'
ID;Nom;Poste
1;Zoé;Développeuse
2;André;Analyste
3;Hélène;Gestionnaire
EOF

RUN tmpdir="$(mktemp -d)" && \
    cat > "${tmpdir}/daten_de.utf8" <<'EOF'
ArtikelID|Name|Beschreibung
1001|Käse|Frischer Gouda
1002|Würstchen|Brühwurst aus Bayern
1003|Apfel|Süßer Elstar
EOF

# Convert the UTF-8 files to Latin-1 and place them where needed
RUN tmpdir="$(mktemp -d)" && \
    cat > "${tmpdir}/clients_es.utf8" <<'EOFCLIENTS'
ID,Nombre,País
1,Ana,Costa Rica
2,José,México
3,María,España
EOFCLIENTS

RUN tmpdir="$(mktemp -d)" && \
    cat > "${tmpdir}/résumé_fr.utf8" <<'EOFRESUME'
ID;Nom;Poste
1;Zoé;Développeuse
2;André;Analyste
3;Hélène;Gestionnaire
EOFRESUME

RUN tmpdir="$(mktemp -d)" && \
    cat > "${tmpdir}/daten_de.utf8" <<'EOFDATEN'
ArtikelID|Name|Beschreibung
1001|Käse|Frischer Gouda
1002|Würstchen|Brühwurst aus Bayern
1003|Apfel|Süßer Elstar
EOFDATEN

# Create all files and convert in one step
RUN set -e && \
    tmpdir="$(mktemp -d)" && \
    printf '%s\n' 'ID,Nombre,País' '1,Ana,Costa Rica' '2,José,México' '3,María,España' > "${tmpdir}/clients_es.utf8" && \
    printf '%s\n' 'ID;Nom;Poste' '1;Zoé;Développeuse' '2;André;Analyste' '3;Hélène;Gestionnaire' > "${tmpdir}/résumé_fr.utf8" && \
    printf '%s\n' 'ArtikelID|Name|Beschreibung' '1001|Käse|Frischer Gouda' '1002|Würstchen|Brühwurst aus Bayern' '1003|Apfel|Süßer Elstar' > "${tmpdir}/daten_de.utf8" && \
    for src in "${tmpdir}"/*.utf8; do \
        base="$(basename "${src}" .utf8)"; \
        iconv -f UTF-8 -t ISO-8859-1 "${src}" > "/home/user/support/incoming/${base}.txt"; \
    done && \
    rm -rf "${tmpdir}" && \
    chmod 0755 /home/user/support/incoming && \
    chmod 0644 /home/user/support/incoming/*.txt

RUN chmod 755 /home/user