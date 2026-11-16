#!/usr/bin/env python3
"""Restore a practice test to its original broken state (to redo it).

    python3 scripts/reset.py 02
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    base = os.path.join(ROOT, "tests")
    matches = sorted(d for d in os.listdir(base) if d.startswith(sys.argv[1]))
    if len(matches) != 1:
        sys.exit("expected exactly one tests/%s* folder, found: %s" % (sys.argv[1], matches))
    name = matches[0]
    broken = os.path.join(ROOT, ".reference", name, "broken")
    for fn in sorted(os.listdir(broken)):
        shutil.copy(os.path.join(broken, fn), os.path.join(base, name, fn))
        print("restored tests/%s/%s" % (name, fn))


if __name__ == "__main__":
    main()
