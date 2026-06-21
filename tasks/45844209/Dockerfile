FROM ubuntu:22.04

# Help text from %help
# This container provides the initial environment for the CI/CD dashboard
# CSV-trimming exercise.
# • Python 3 and pytest are installed.
# • The directory /home/user/ci_cd contains build_stats.csv with the exact
#   dataset required by the assignment.

LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for CI/CD CSV trimming exercise with pytest pre-installed."

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/ci_cd && \
    chmod 0755 /home/user/ci_cd

RUN cat >/home/user/ci_cd/build_stats.csv <<'EOF'
BuildID,Branch,CommitHash,Author,Status,DurationSec,ArtifactsSizeMB,Timestamp
101,main,ab12cd3,alice,success,245,120,2023-08-23T10:15:31Z
102,develop,bc34de5,bob,failed,130,0,2023-08-23T10:20:12Z
103,main,cd56ef7,charlie,success,300,98,2023-08-23T10:50:45Z
104,hotfix,ef78gh9,dana,success,210,110,2023-08-23T11:15:02Z
EOF

RUN chmod 0644 /home/user/ci_cd/build_stats.csv && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:${PATH}