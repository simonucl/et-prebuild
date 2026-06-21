FROM ubuntu:22.04

# 1. OS packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Python tooling
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# 3. Non-root user (UID 1000) that will run inside the container
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 user; \
    fi

# 4. SQLite database setup
RUN mkdir -p /home/user/support/db

RUN sqlite3 /home/user/support/db/shop.db <<'SQL'
CREATE TABLE customers (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount      REAL NOT NULL,
    status      TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

INSERT INTO customers (id, name, email, created_at) VALUES
    (1, 'Alice Smith',   'alice@example.com',   '2023-01-03 11:34:21'),
    (2, 'Bob Johnson',   'bob@example.com',     '2023-02-18 09:12:55'),
    (3, 'Charlie Brown', 'charlie@example.com', '2023-03-22 17:49:07');

INSERT INTO orders (id, customer_id, amount, status, created_at) VALUES
    (1, 1, 120.50, 'OPEN',      '2023-04-01 12:00:00'),
    (2, 2,  89.99, 'SHIPPED',   '2023-04-02 14:00:00'),
    (3, 3,  45.00, 'SHIPPED',   '2023-04-03 16:30:00'),
    (4, 1,  67.25, 'CANCELLED', '2023-04-04 18:45:00'),
    (5, 2, 199.95, 'OPEN',      '2023-04-05 10:15:00');
SQL

# 5. Ownership & permissions
RUN chown -R 1000:1000 /home/user && \
    chmod -R 755 /home/user

# 6. Ensure diagnostic directory does NOT exist yet
RUN rm -rf /home/user/support/diag || true

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1