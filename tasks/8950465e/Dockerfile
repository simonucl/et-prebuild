FROM ubuntu:22.04

# Help:
# This Apptainer image provides the initial filesystem state for the
# "employee report" assignment. It contains the three required source
# data files in /home/user/data and has pytest pre-installed for
# automated grading.

LABEL Author="task-preparer"
LABEL Description="Container with initial dataset and pytest for employee report assignment."

ENV PYTHONIOENCODING="utf-8"
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data

RUN cat <<'EOF' > /home/user/data/people.txt
1,John,Doe,Engineering
2,Jane,Smith,Marketing
3,Bob,Johnson,Sales
4,Alice,Williams,Engineering
5,Mike,Brown,Support
EOF

RUN cat <<'EOF' > /home/user/data/salaries.txt
1,90000,5000,2023
2,80000,4000,2023
3,75000,3000,2023
4,95000,6000,2023
5,60000,2000,2023
EOF

RUN cat <<'EOF' > /home/user/data/addresses.txt
1,Seattle,WA,98101
2,Portland,OR,97201
3,San Francisco,CA,94105
4,Boston,MA,02108
5,Austin,TX,73301
EOF

RUN chmod 755 /home/user /home/user/data && \
    chmod 644 /home/user/data/*.txt