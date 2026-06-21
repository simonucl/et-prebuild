FROM ubuntu:22.04

LABEL Author="Apptainer Task Prep Bot"
LABEL Description="Container providing initial state for the web-analytics cut/paste task"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/projects/web_analytics/raw && \
    chmod -R 0777 /home/user

RUN cat > /home/user/projects/web_analytics/raw/analytics_2023-10-15.csv << 'EOF'
Date,PageViews,UniqueVisitors,BounceRate,AvgTimeOnPage
2023-10-10,1450,675,0.42,00:03:21
2023-10-11,1320,598,0.38,00:03:10
2023-10-12,1703,840,0.41,00:03:45
2023-10-13,1250,560,0.40,00:03:05
2023-10-14,1800,910,0.39,00:03:50
EOF

RUN chmod 0644 /home/user/projects/web_analytics/raw/analytics_2023-10-15.csv

ENV HOME=/home/user

WORKDIR /home/user

CMD ["bash", "-l"]