# Build a standards-compliant wheel

The source tree for a small Python package already exists at:

`/home/user/work/packet_sentinel`

Create a wheel file at exactly:

`/home/user/work/packet_sentinel/dist/packet_sentinel-1.2.0-py3-none-any.whl`

Requirements:

* The wheel must be a valid ZIP-format Python wheel for package name `packet-sentinel`, version `1.2.0`, pure Python, tag `py3-none-any`.
* Include the package files under `packet_sentinel/`, including `rules/defaults.toml` and `py.typed`.
* Include a console entry point named `packet-sentinel` that resolves to `packet_sentinel.cli:main`.
* Include correct `METADATA`, `WHEEL`, `entry_points.txt`, and `RECORD` files under `packet_sentinel-1.2.0.dist-info/`.
* `RECORD` must contain SHA-256 hashes and byte sizes for every wheel member except `RECORD` itself, whose hash and size fields must be empty.
* The wheel archive should use ordinary deflated ZIP members and stable wheel-style permissions.

Do not modify or remove the source files. The final answer is the wheel file in `dist/`; no extra report is needed.
