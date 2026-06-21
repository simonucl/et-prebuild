# Converted from Apptainer definition file
FROM ubuntu:22.04

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Post section
RUN set -eux && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir -U pytest

RUN mkdir -p /home/user/pt_reports

RUN cat > /home/user/pt_reports/scan_results_critical.txt <<'EOF'
CVE-2023-1234: OpenSSH user enumeration vulnerability
CVE-2022-3456: Apache Struts remote code execution
CVE-2021-0001: Sample vulnerability
EOF

RUN chmod 644 /home/user/pt_reports/scan_results_critical.txt && \
    chmod 755 /home/user/pt_reports && \
    chmod 755 /home/user

RUN if [ -d /home/user/archives ]; then rm -rf /home/user/archives; fi

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]