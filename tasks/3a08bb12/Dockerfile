FROM ubuntu:22.04

# Author Incident-FS-Prep
# Description "Base image for the Incident directory hardening & permission audit exercise."

LABEL Author="Incident-FS-Prep" \
      Description="Base image for the Incident directory hardening & permission audit exercise."

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN useradd -m -u 1000 -s /bin/bash user

RUN INCIDENT_DIR=/home/user/incident_reports && \
    mkdir -p "$INCIDENT_DIR" && \
    printf 'PLACEHOLDER: do not modify\n' > "$INCIDENT_DIR/report_2023_11_15.txt" && \
    chmod 0755 "$INCIDENT_DIR" && \
    chmod 0644 "$INCIDENT_DIR/report_2023_11_15.txt" && \
    chown -R user:user /home/user

RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

CMD ["/bin/bash"]