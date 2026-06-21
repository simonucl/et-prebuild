FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Environment for observability engineer regex filtering exercise."

# Set non-interactive apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Ensure Python and pip are on the PATH
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Install packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading suite
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create the required directory tree
RUN mkdir -p /home/user/observability/input

# Create the synthetic log file
RUN cat >/home/user/observability/input/app.log <<'EOF'
2023-07-19 10:13:45,123 INFO  PaymentsService - Starting reconciliation
2023-07-19 10:13:45,456 ERROR PaymentsService - Failed to reconcile invoice 8745
2023-07-19 11:07:12,789 WARN  AuthService - Token expired for user 102
2023-07-19 11:07:15,001 INFO  AuthService - Token refreshed for user 102
2023-07-20 09:03:05,321 ERROR OrdersService - Order 5561 could not be processed
2023-07-20 09:03:06,555 INFO  OrdersService - Retry queued for order 5561
2023-07-20 12:47:17,678 ERROR InventoryService - Stock level mismatch for SKU 887
2023-07-20 12:47:18,999 WARN  InventoryService - Retrying stock update
2023-07-20 20:00:00,555 ERROR AuthService - Authentication DB unreachable
2023-07-21 08:22:55,111 INFO  PaymentsService - Reconciliation complete
2023-07-21 08:23:00,222 ERROR PaymentsService - Payment gateway timeout
2023-07-21 14:15:42,333 INFO  OrdersService - Order 5561 processed successfully
2023-07-21 14:16:42,444 ERROR OrdersService - Refund failed for order 5561
EOF

# Make sure everything is world-readable; the runtime user will not have root
RUN chmod -R a+rX /home/user/observability && \
    chmod 755 /home/user

# Set working directory
WORKDIR /home/user

# Help information (as comments):
# This container provides the starting filesystem state for the
# "observability engineer" exercise.  The synthetic application log
# is located at:
#   /home/user/observability/input/app.log
#
# Students must generate filtered output files under:
#   /home/user/observability/output
#
# Pytest is installed for automatic grading.