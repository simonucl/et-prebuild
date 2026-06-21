FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory layout required by the tests
RUN mkdir -p /home/user/finops/raw_reports/year=2023 && \
    mkdir -p /home/user/finops/raw_reports/year=2024 && \
    touch /home/user/finops/raw_reports/year=2023/cost_report_2023-11.csv && \
    touch /home/user/finops/raw_reports/year=2023/cost_report_2023-12.csv && \
    touch /home/user/finops/raw_reports/year=2024/cost_report_2024-01.csv && \
    touch /home/user/finops/raw_reports/year=2024/cost_report_2024-02.csv && \
    touch /home/user/finops/raw_reports/year=2024/cost_report_2024-03.csv && \
    chmod -R a+rwx /home/user/finops

# Environment settings
ENV PYTHONUNBUFFERED=1

RUN chmod 755 /home/user

CMD ["bash"]