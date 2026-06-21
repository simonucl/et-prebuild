FROM ubuntu:22.04

# Base system and Python tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Python packages required for the grading harness
RUN pip3 install --no-cache-dir pytest

# Prepare the fixed log file
RUN mkdir -p /home/user/project

RUN cat > /home/user/project/app.log <<'EOF'
2023-09-30T10:15:32Z INFO AuthService User login successful for id=42
2023-09-30T10:16:02Z ERROR AuthService Invalid credentials for user id=43
2023-09-30T10:17:45Z WARN PaymentService Payment took longer than expected txn=987
2023-09-30T10:18:12Z ERROR PaymentService Failed to authorize payment txn=988
2023-09-30T10:18:15Z ERROR PaymentService Failed to authorize payment txn=990
2023-09-30T10:19:05Z INFO NotificationService Email sent to user id=42
2023-09-30T10:20:22Z ERROR NotificationService SMTP connection timeout
2023-09-30T10:21:33Z ERROR AuthService Invalid credentials for user id=44
2023-09-30T10:22:47Z ERROR AuthService Invalid credentials for user id=45
2023-09-30T10:23:58Z INFO AuthService User logout id=42
2023-09-30T10:25:04Z ERROR PaymentService Failed to authorize payment txn=991
EOF

RUN chmod 644 /home/user/project/app.log && \
    chmod 777 /home/user/project && \
    chmod 755 /home/user

ENV PATH="/usr/bin:$PATH"

LABEL Author="Container build generated for log-analysis task (Apptainer)"
LABEL Description="Provides initial state with fixed log file and pytest installed."