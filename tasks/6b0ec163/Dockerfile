FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Setup Script"
LABEL Description="Container for micro-benchmark security scan task with pytest pre-installed."

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# System packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        build-essential \
        gcc \
        make \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python packages
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Project setup
RUN mkdir -p /home/user/perf_project

# main.c
RUN cat > /home/user/perf_project/main.c <<'EOF'
#include <stdio.h>
#include <string.h>
#include "util.h"

int main(int argc, char *argv[]) {
    char buffer[64];
    if(argc > 1) {
        strcpy(buffer, argv[1]); // insecure call
    } else {
        strcpy(buffer, "default"); // insecure call
    }
    char out[128];
    sprintf(out, "Input was: %s", buffer); // insecure call
    chmod 755 /home/user

    puts(out);
    echo_user_input();
    return 0;
}
EOF

# util.c
RUN cat > /home/user/perf_project/util.c <<'EOF'
#include <stdio.h>
#include <string.h>
#include "util.h"

void echo_user_input(void) {
    char buffer[128];
    puts("Enter something: ");
    gets(buffer); // insecure call
    printf("You said: %s\n", buffer);
}
EOF

# util.h
RUN cat > /home/user/perf_project/util.h <<'EOF'
void echo_user_input(void);
EOF

# Permissions – allow the unprivileged runtime user to write results
RUN chmod -R a+rwX /home/user