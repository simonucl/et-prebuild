FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Environment prepared for the \"DataCleaner\" log-processing task."

# Base tooling
RUN set -e && \
    apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir pytest

# Prepare directory tree accessible to the learner
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create the log files and package them
RUN set -e && \
    TMPDIR="$(mktemp -d)" && \
    mkdir -p "${TMPDIR}/logs" && \
    # app1.log
    printf "2023-07-01 10:02:15\tINFO\tDataLoader\tStarting load\n"               >  "${TMPDIR}/logs/app1.log" && \
    printf "2023-07-01 10:05:33\tERROR\tDataCleaner\tNull value encountered\n"    >> "${TMPDIR}/logs/app1.log" && \
    printf "2023-07-02 11:42:07\tWARN\tDataCleaner\tImputed missing values\n"     >> "${TMPDIR}/logs/app1.log" && \
    printf "2023-07-03 08:15:44\tERROR\tDataCleaner\tOut-of-range value\n"        >> "${TMPDIR}/logs/app1.log" && \
    # app2.log
    printf "2023-07-01 14:22:05\tERROR\tDataCleaner\tNull value encountered\n"     > "${TMPDIR}/logs/app2.log" && \
    printf "2023-07-02 15:11:23\tINFO\tDataLoader\tLoad complete\n"               >> "${TMPDIR}/logs/app2.log" && \
    printf "2023-07-03 16:35:55\tERROR\tDataCleaner\tOut-of-range value\n"        >> "${TMPDIR}/logs/app2.log" && \
    # app3.log
    printf "2023-07-01 09:00:00\tINFO\tSystem\tBoot\n"                             > "${TMPDIR}/logs/app3.log" && \
    printf "2023-07-02 12:34:56\tERROR\tDataCleaner\tNull value encountered\n"    >> "${TMPDIR}/logs/app3.log" && \
    printf "2023-07-04 18:48:10\tERROR\tOtherModule\tSomething bad\n"             >> "${TMPDIR}/logs/app3.log" && \
    printf "2023-07-04 19:00:00\tERROR\tDataCleaner\tOut-of-range value\n"        >> "${TMPDIR}/logs/app3.log" && \
    # Archive placement
    mkdir -p /home/user/datasets && \
    tar -czf /home/user/datasets/log_archive.tar.gz -C "${TMPDIR}" logs && \
    chmod 0755 /home/user/datasets && \
    chmod 0644 /home/user/datasets/log_archive.tar.gz && \
    # Clean up temporary build directory
    rm -rf "${TMPDIR}"

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Docker container for the DataCleaner log-processing task. No default action. Invoke shell or specific commands as needed."]