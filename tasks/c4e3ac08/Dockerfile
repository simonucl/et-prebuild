FROM ubuntu:22.04

# Labels
LABEL Author="Autograder Setup"
LABEL Description="Challenge container with predefined timezone, locale, pytest, and directory skeleton."

# Set environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV TZ=Etc/UTC
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install required packages
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        locales \
        tzdata \
        python3-pip \
        ca-certificates

# Configure system locale to C.UTF-8
RUN sed -i 's/^# *\(C\.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen C.UTF-8 && \
    update-locale LANG=C.UTF-8 && \
    echo 'LANG=C.UTF-8' > /etc/default/locale && \
    echo 'LC_ALL=C.UTF-8' >> /etc/default/locale

# Configure system time-zone to Etc/UTC
RUN ln -sf /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo 'Etc/UTC' > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# Python tooling (pytest for the grader)
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Prepare the directory structure expected by the challenge
RUN mkdir -p /home/user/logs && \
    chmod 0755 /home /home/user /home/user/logs || true

# Clean up APT caches to keep image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

# This container is prepared for the "system context" challenge.
# • Time-zone: Etc/UTC
# • Locale:    C.UTF-8
# • Pytest installed for internal grading.
# Directory /home/user/logs (0755) is pre-created for the learner.