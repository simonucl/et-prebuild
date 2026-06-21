FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/vulnscan && \
    chmod 755 /home/user && \
    chmod 755 /home/user/vulnscan

RUN DB_PATH="/home/user/vulnscan/scan_results.db" && \
    sqlite3 "${DB_PATH}" <<'SQL'
CREATE TABLE vulnerabilities(
    host_ip   TEXT,
    port      INTEGER,
    service   TEXT,
    cve_id    TEXT,
    severity  TEXT
);

INSERT INTO vulnerabilities (host_ip, port, service, cve_id, severity) VALUES
('192.168.1.10', 22,  'ssh',   'CVE-2018-15473', 'HIGH'),
('192.168.1.12', 80,  'http',  'CVE-2020-5902',  'HIGH'),
('192.168.1.20', 445, 'smb',   'CVE-2017-0144', 'HIGH'),
('192.168.1.30', 21,  'ftp',   'CVE-2021-41617', 'MEDIUM'),
('10.0.0.5',    3306,'mysql', 'CVE-2016-6662',  'HIGH');
SQL

RUN chmod 644 /home/user/vulnscan/scan_results.db

ENV PATH=/usr/local/bin:$PATH

CMD ["bash"]