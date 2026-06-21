# Author firewall-observability-setup
# Description: Container prepared for firewall configuration exercise with pytest pre-installed.
# Help:
# This Docker image sets up the initial state for the “Prometheus / Grafana / node-exporter firewall” exercise.
# It provides:
#   • /home/user/firewall_configs/iptables_prometheus.rules
#   • /home/user/report_firewall.log
#   • pytest (installed via pip)
# No iptables rules are applied—only staged for later use by privileged operators.

FROM ubuntu:22.04

LABEL Author="firewall-observability-setup" \
      Description="Container prepared for firewall configuration exercise with pytest pre-installed."

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/firewall_configs

RUN cat > /home/user/firewall_configs/iptables_prometheus.rules <<'RULES'
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -p tcp --dport 22   -j ACCEPT
-A INPUT -p tcp --dport 9090 -j ACCEPT
-A INPUT -p tcp --dport 3000 -j ACCEPT
-A INPUT -p tcp --dport 9100 -j ACCEPT
COMMIT
RULES

RUN cat > /home/user/report_firewall.log <<'REPORT'
22,ALLOWED
9090,ALLOWED
3000,ALLOWED
9100,ALLOWED
3306,DENIED
REPORT

RUN chmod 755 /home/user && \
    chmod 755 /home/user/firewall_configs && \
    chmod 644 /home/user/firewall_configs/iptables_prometheus.rules && \
    chmod 644 /home/user/report_firewall.log