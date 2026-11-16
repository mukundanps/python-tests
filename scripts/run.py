#!/usr/bin/env python3
"""Run one practice test and print the score.

    python3 scripts/run.py 02          # run test 02
    python3 scripts/run.py 02 -v       # verbose (per-test names)
    python3 scripts/run.py 02 --log    # also append the score to PROGRESS.md
"""
import datetime
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_test_dir(prefix):
    base = os.path.join(ROOT, "tests")
    matches = sorted(d for d in os.listdir(base) if d.startswith(prefix))
    if len(matches) != 1:
        sys.exit("expected exactly one tests/%s* folder, found: %s" % (prefix, matches))
    return matches[0], os.path.join(base, matches[0])


def run_dir(path, verbosity=1):
    """Run every test_*.py in `path`; return (passed, total)."""
    sys.path.insert(0, path)
    try:
        suite = unittest.TestLoader().discover(path, pattern="test_*.py", top_level_dir=path)
        result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    finally:
        sys.path.remove(path)
    bad = len(result.failures) + len(result.errors)
    return result.testsRun - bad, result.testsRun


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        sys.exit(__doc__)
    name, path = find_test_dir(args[0])
    passed, total = run_dir(path, verbosity=2 if "-v" in sys.argv else 1)
    print("\nSCORE %s: %d / %d" % (name, passed, total))
    if "--log" in sys.argv:
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(os.path.join(ROOT, "PROGRESS.md"), "a") as f:
            f.write("| %s | %s | %d / %d | |\n" % (stamp, name, passed, total))
        print("logged to PROGRESS.md")


if __name__ == "__main__":
    main()
