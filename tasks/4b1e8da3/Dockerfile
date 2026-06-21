FROM ubuntu:22.04

# Labels
LABEL Author="AI_Generated"
LABEL Description="Environment for FinOps Q2-2023 patch-application exercise"

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends patch python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip pytest

RUN mkdir -p /home/user/finops_reports

RUN cat > /home/user/finops_reports/cost_report_Q2_2023.csv << 'EOF'
Project,Service,Month,CostUSD
ProjectA,Compute,2023-04,1500.00
ProjectA,Storage,2023-04,200.00
ProjectB,Compute,2023-04,1800.00
ProjectB,Database,2023-04,600.00
EOF

RUN cat > /home/user/finops_reports/cost_report_Q2_2023.patch << 'EOF'
--- cost_report_Q2_2023.csv	2023-05-01 12:00:00.000000000 +0000
+++ cost_report_Q2_2023.csv	2023-05-02 12:00:00.000000000 +0000
@@ -1,5 +1,6 @@
 Project,Service,Month,CostUSD
 ProjectA,Compute,2023-04,1500.00
-ProjectA,Storage,2023-04,200.00
+ProjectA,Storage,2023-04,150.00
 ProjectB,Compute,2023-04,1800.00
-ProjectB,Database,2023-04,600.00
+ProjectB,Database,2023-04,450.00
+ProjectC,Analytics,2023-04,300.00
EOF

RUN chmod 0777 /home/user/finops_reports && \
    chmod 0666 /home/user/finops_reports/cost_report_Q2_2023.csv && \
    chmod 0644 /home/user/finops_reports/cost_report_Q2_2023.patch && \
    chmod 0755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD /bin/sh -c "echo 'Container for FinOps Q2-2023 patch exercise.' && echo 'Navigate to /home/user/finops_reports to begin.'"