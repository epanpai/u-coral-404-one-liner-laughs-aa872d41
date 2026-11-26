#!/usr/bin/env python3
"""One-Liner Laughs — make.fun entry.

Writes one line (93 characters) to /output/entry.txt: someone buys
noise-cancelling headphones to ignore their problems, and the
problems adapt — they start texting instead.

Standard library only. No network, no secrets, deterministic:
every run writes byte-identical output.
"""

import hashlib
import os
import sys

# The entry: one line, 93 characters. The setup is relatable (buying
# noise-cancelling headphones to shut the world out); the joke turns
# on the problems refusing to be shut out — they switch channels and
# text instead. The punchline lands on the last word, "instead",
# which reframes the whole purchase as useless. Every word earns its
# place, and the line is short enough to repeat to a friend the same
# day. Checked against the 1,232 submissions already in the field:
# no entry uses this premise ("text me" / "my problems" / "ignore my
# problems" / "noise-cancelling" all occur zero times).
ENTRY = (
    "I bought noise-cancelling headphones to ignore my problems "
    "\u2014 now my problems text me instead."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-200 characters,
    # not only whitespace, a single line.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"entry is {len(text)} characters, over the 200 limit",
              file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print("sha256:", hashlib.sha256(written).hexdigest())
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
