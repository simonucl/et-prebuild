FROM ubuntu:22.04

# Help/labels from %labels
LABEL Author="Apptainer exercise generator"
LABEL Description="Base image for legacy-customer migration task (pytest pre-installed)"

# Post section
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data/source

RUN cat <<'EOF' > /home/user/data/source/customers_legacy.csv
customer_id,name,age,signup_date
1,Alice,30,2021-01-05
2,Bob,17,2022-07-12
3,Charlie,25,2019-11-23
4,David,15,2020-02-14
5,Eva,40,2018-06-30
6,Frank,22,2023-03-01
EOF

RUN chmod -R a+rX /home/user && \
    chmod -R a+w /home/user /home/user/data /home/user/data/source

# Environment section
RUN chmod 755 /home/user
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8