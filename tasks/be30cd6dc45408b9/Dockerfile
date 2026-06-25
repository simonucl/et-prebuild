FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y bash python3 && rm -rf /var/lib/apt/lists/*

RUN python3 - <<'PY'
from pathlib import Path

root = Path("/app")
(root / "raw").mkdir(parents=True, exist_ok=True)
(root / "config").mkdir(parents=True, exist_ok=True)
(root / "out").mkdir(parents=True, exist_ok=True)

(root / "raw" / "gateway_alpha.csv").write_text(
    "payment_id,merchant,amount,currency,status,event_time,settled_at\n"
    "pay_1001,Northwind,\"$1,250.40\",USD,SETTLED,2026-06-01T14:15:00Z,2026-06-01T14:20:00Z\n"
    "pay_1002,Northwind,-15.99,USD,REFUND,2026-06-02T09:00:00Z,2026-06-02T09:05:00Z\n"
    "pay_1003,Contoso,72.10,EUR,paid,2026-06-02T12:30:00Z,2026-06-02T12:34:00Z\n"
    "pay_1004,Contoso,18.00,USD,voided,2026-06-02T13:00:00Z,\n"
    "pay_1005,Northwind,9.995,USD,paid,2026-06-03T10:00:00Z,2026-06-03T10:01:00Z\n"
    ",Tailspin,7.00,USD,paid,2026-06-03T11:00:00Z,2026-06-03T11:02:00Z\n",
    encoding="utf-8",
)

(root / "raw" / "gateway_beta.csv").write_text(
    "payment_id,merchant,amount,currency,status,event_time,settled_at\n"
    "pay_1003,Contoso,73.10,EUR,settled,2026-06-02T12:45:00Z,2026-06-02T12:50:00Z\n"
    "pay_1006,Tailspin,\"2,500\",USD,SETTLED,2026-06-03T08:00:00Z,2026-06-03T08:05:00Z\n"
    "pay_1007,Tailspin,4.20,GBP,SETTLED,2026-06-03T09:00:00Z,2026-06-03T09:05:00Z\n"
    "pay_1008,Northwind,3.50,USD,chargeback,2026-06-03T12:00:00Z,\n"
    "pay_1002,Northwind,15.99,USD,refunded,2026-06-02T09:30:00Z,2026-06-02T09:35:00Z\n",
    encoding="utf-8",
)

(root / "config" / "status-map.json").write_text(
    '{"SETTLED":"settled","settled":"settled","paid":"settled",'
    '"REFUND":"refunded","refunded":"refunded","voided":"failed",'
    '"chargeback":"refunded"}\n',
    encoding="utf-8",
)

(root / "README.raw.txt").write_text(
    "Raw gateway exports are immutable inputs. Build derived artifacts in /app/out only.\n",
    encoding="utf-8",
)
PY
