FROM ubuntu:22.04

# Help text from Apptainer %labels Author/Description
LABEL Author="container-builder"
LABEL Description="Environment for simple integrity-alert monitoring task"

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip install --no-cache-dir -q pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/watched

RUN chmod 0777 /home/user

RUN printf 'hello' > /home/user/watched/critical_report.txt && \
    chmod 0755 /home/user/watched && \
    chmod 0644 /home/user/watched/critical_report.txt

RUN chmod 755 /home/user