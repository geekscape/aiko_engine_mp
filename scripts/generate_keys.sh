#!/usr/bin/env python3

import os
import sys

def main(pathname, start, count):
    if not pathname:
        pathname = "."

    for index in range(start, start + count):
        key = os.urandom(32)
        key = "".join(hex(digit)[-2:] for digit in key)
        with open(f"{pathname}/keys_{index:04d}.db", "w") as file:
          file.write(f"key={key}\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Usage: generate_keys.py pathname start count")
    pathname = sys.argv[1]
    start = int(sys.argv[2])
    count = int(sys.argv[3])
    try:
        main(pathname, start, count)
    except KeyboardInterrupt:
        raise SystemExit("KeyboardInterrupt: abort !")
