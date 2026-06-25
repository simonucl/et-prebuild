import base64
import csv
import hashlib
import shutil
import zipfile
from pathlib import Path

base = Path("/home/user/simple_repo")
wheelhouse = base / "wheelhouse"
public = base / "public"
shutil.rmtree(base, ignore_errors=True)
wheelhouse.mkdir(parents=True)
(public / "simple" / "stale-project").mkdir(parents=True)
(public / "packages").mkdir(parents=True)
(public / "simple" / "index.html").write_text("<html><body>stale index</body></html>\n")
(public / "simple" / "stale-project" / "index.html").write_text("stale\n")
(public / "packages" / "old-build.whl").write_text("remove me\n")
(base / "README.txt").write_text(
    "Build the static simple repository in /home/user/simple_repo/public from the wheels in wheelhouse.\n"
)


def b64sha(data: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")


def wheel_record(rows):
    out = []
    for path, data in rows:
        out.append(f"{path},sha256={b64sha(data)},{len(data)}")
    out.append(f"{rows[-1][0].rsplit('/', 1)[0]}/RECORD,,")
    return ("\n".join(out) + "\n").encode()


def make_wheel(filename, dist_info, metadata_name, version, summary, package_dir):
    metadata = (
        "Metadata-Version: 2.1\n"
        f"Name: {metadata_name}\n"
        f"Version: {version}\n"
        f"Summary: {summary}\n"
        "Requires-Python: >=3.10\n"
        "\n"
    ).encode()
    wheel = (
        "Wheel-Version: 1.0\n"
        "Generator: staged-offline-wheelhouse\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n"
        "\n"
    ).encode()
    init = f"__version__ = {version!r}\n".encode()
    rows = [
        (f"{package_dir}/__init__.py", init),
        (f"{dist_info}/METADATA", metadata),
        (f"{dist_info}/WHEEL", wheel),
    ]
    record = wheel_record(rows)
    rows.append((f"{dist_info}/RECORD", record))
    with zipfile.ZipFile(wheelhouse / filename, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for arcname, data in rows:
            info = zipfile.ZipInfo(arcname, (2024, 6, 25, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)


make_wheel(
    "Acme_Widget-1.0.0-py3-none-any.whl",
    "Acme_Widget-1.0.0.dist-info",
    "Acme.Widget",
    "1.0.0",
    "Legacy widget helpers",
    "acme_widget",
)
make_wheel(
    "Acme_Widget-1.2.0-py3-none-any.whl",
    "Acme_Widget-1.2.0.dist-info",
    "Acme.Widget",
    "1.2.0",
    "Current widget helpers",
    "acme_widget",
)
make_wheel(
    "data_parser-0.9.1-py3-none-any.whl",
    "data_parser-0.9.1.dist-info",
    "data-parser",
    "0.9.1",
    "CSV and TSV parser utilities",
    "data_parser",
)
make_wheel(
    "TLS_Audit-2.0.0-py3-none-any.whl",
    "TLS_Audit-2.0.0.dist-info",
    "TLS_Audit",
    "2.0.0",
    "Certificate audit helpers",
    "tls_audit",
)

with (base / "expected_projects.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["normalized", "display"])
    writer.writerow(["acme-widget", "Acme.Widget"])
    writer.writerow(["data-parser", "data-parser"])
    writer.writerow(["tls-audit", "TLS_Audit"])
