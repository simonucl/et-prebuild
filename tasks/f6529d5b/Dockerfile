FROM ubuntu:22.04

# Help section from the definition file:
# Converted from Apptainer localimage bootstrap using ubuntu:22.04 as base

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

RUN set -eux \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip gzip \
    && pip3 install --no-cache-dir pytest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/source_files

RUN cat <<'EOF' > /home/user/source_files/financials_Q4.csv
Dept,Spend,Quarter
IT,23500,Q4
HR,8200,Q4
Finance,12300,Q4
EOF

RUN cat <<'EOF' > /home/user/source_files/policy_doc.txt
All employees must adhere to the security compliance guidelines set forth in section 9.2.
EOF

RUN echo -n "snapshot-2023Q4" | gzip -c > /home/user/source_files/infra_snapshot.tar.gz

RUN chmod 644 /home/user/source_files/financials_Q4.csv \
    && chmod 644 /home/user/source_files/policy_doc.txt \
    && chmod 644 /home/user/source_files/infra_snapshot.tar.gz \
    && chmod 755 /home/user