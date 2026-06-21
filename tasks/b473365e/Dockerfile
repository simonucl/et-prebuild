# syntax=docker/dockerfile:1
# Author: FinOps-Prep
# Description: Base image for FinOps CLI alignment task – provides raw CSV data and pytest.

FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sudo && \
    pip install --no-cache-dir pytest && \
    if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user; \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

RUN set -e && \
    BASEDIR=/home/user/finops && \
    RAWDIR=${BASEDIR}/raw && \
    WORKDIR=${BASEDIR}/work && \
    OUTDIR=${BASEDIR}/output && \
    mkdir -p "${RAWDIR}" "${WORKDIR}" "${OUTDIR}"

RUN BASEDIR=/home/user/finops && \
    RAWDIR=${BASEDIR}/raw && \
    cat > "${RAWDIR}/usage_report.csv" <<'EOF'
Service,ResourceID,HoursUsed,Region
EC2,i-123456,720,us-east-1
S3,bucket-abc,0,us-east-1
RDS,db-654321,300,us-west-2
EOF

RUN BASEDIR=/home/user/finops && \
    RAWDIR=${BASEDIR}/raw && \
    cat > "${RAWDIR}/pricing.csv" <<'EOF'
Service,PricePerHourUSD,Region,LastUpdated
EC2,0.023,us-east-1,2023-09-01
S3,0.000,us-east-1,2023-09-01
RDS,0.250,us-west-2,2023-09-01
EOF

RUN BASEDIR=/home/user/finops && \
    RAWDIR=${BASEDIR}/raw && \
    WORKDIR=${BASEDIR}/work && \
    OUTDIR=${BASEDIR}/output && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user && \
    chmod 755 "${BASEDIR}" "${RAWDIR}" "${WORKDIR}" "${OUTDIR}" && \
    chmod 644 "${RAWDIR}"/*.csv

# Default run behavior: open an interactive shell as non-root user
CMD ["sudo", "-u", "user", "-E", "/bin/bash"]