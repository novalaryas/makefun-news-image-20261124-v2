#!/usr/bin/env python3
"""make.fun news-image-20261124 entry.

Builds the broadsheet front page "THE WORLD" — a summary of
Tuesday 24 November 2026's world news — as a single PNG image.

The page is rendered text (see gen_image.py in the work notes), shipped
here as image.png. This program just places those exact bytes at the
output path. It is deterministic and offline: no network, no clock,
no randomness, so every run writes identical bytes.
"""

import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "image.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def build(output_dir: str) -> Path:
    """Copy image.png to <output_dir>/entry.png; return the target path."""
    data = IMAGE.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("error: image.png is not a PNG file")
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    target.write_bytes(data)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return target


def main(argv) -> int:
    out = argv[1] if len(argv) > 1 else None
    import os

    build(out or os.environ.get("ENTRY_OUTPUT_DIR", "/output"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
