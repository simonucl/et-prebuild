# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author="Apptainer Setup Script"
# Description="Environment for FinOps archival task with pytest pre-installed."

ENV CLOUD_DIR=/home/user/cloud_reports

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN mkdir -p "$CLOUD_DIR"

RUN for m in $(seq -w 1 12); do \
        printf "Month,TotalUSD\n2023-%s,1000\n" "$m" > "$CLOUD_DIR/cost_report_2023-${m}.csv"; \
    done

RUN printf "Year,TotalUSD\n2023,12000\n" > "$CLOUD_DIR/summary_2023.csv"

RUN echo "README for 2023 cloud cost reports. Do not modify." > "$CLOUD_DIR/README.txt"

RUN chmod 755 /home/user && chown -R user:user /home/user

CMD ["/bin/bash"]