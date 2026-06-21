FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/migration_data

RUN cat > /home/user/migration_data/services.tsv <<'EOF'
service_id	service_name	environment	owner	port	status
1001	auth-api	prod	team-alpha	443	active
1002	payment-api	stage	team-beta	8080	active
1003	legacy-mq	prod	team-legacy	61616	deprecated
1004	catalog-web	dev	team-gamma	80	active
1005	orders-api	prod	team-alpha	443	migrate
1006	shipping-api	prod	team-beta	443	migrate
1007	analytics-batch	stage	team-delta	9000	migrate
1008	billing-web	prod	team-gamma	443	active
EOF

RUN chmod 664 /home/user/migration_data/services.tsv && \
    chmod 775 /home/user/migration_data

RUN chmod 755 /home/user

LABEL Author="example"
LABEL Description="Initial state for migration task – source TSV provided, targets absent."