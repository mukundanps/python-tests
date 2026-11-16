#!/usr/bin/env python3
"""Check that every practice test is well formed. Run after adding a test.

For each tests/<name>/ it checks, in a temp copy (your work is not touched):
  1. the reference solution passes every test
  2. the original broken version fails some tests but still passes some

    python3 scripts/verify.py          # all tests
    python3 scripts/verify.py 03       # one test
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def score(test_dir, overrides):
    """Copy tests + overrides ({filename: source path}) to a temp dir, run, return (passed, total)."""
    tmp = tempfile.mkdtemp()
    try:
        for fn in os.listdir(test_dir):
            if fn.startswith("test_") and fn.endswith(".py"):
                shutil.copy(os.path.join(test_dir, fn), tmp)
        for fn, src in overrides.items():
            shutil.copy(src, os.path.join(tmp, fn))
        code = (
            "import sys, unittest\n"
            "s = unittest.TestLoader().discover('.', pattern='test_*.py')\n"
            "r = unittest.TextTestRunner(stream=open('/dev/null', 'w')).run(s)\n"
            "print(r.testsRun - len(r.failures) - len(r.errors), r.testsRun)\n"
        )
        out = subprocess.run(
            [sys.executable, "-c", code], cwd=tmp, capture_output=True, text=True, timeout=120
        )
        passed, total = out.stdout.split()[-2:]
        return int(passed), int(total)
    finally:
        shutil.rmtree(tmp)


def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 else ""
    ok = True
    for name in sorted(os.listdir(os.path.join(ROOT, "tests"))):
        if not name.startswith(prefix):
            continue
        test_dir = os.path.join(ROOT, "tests", name)
        ref_dir = os.path.join(ROOT, ".reference", name)
        solutions = {
            fn[len("solution_"):]: os.path.join(ref_dir, fn)
            for fn in os.listdir(ref_dir)
            if fn.startswith("solution_")
        }
        broken_dir = os.path.join(ref_dir, "broken")
        broken = {fn: os.path.join(broken_dir, fn) for fn in os.listdir(broken_dir)}
        sp, st = score(test_dir, solutions)
        bp, bt = score(test_dir, broken)
        good = sp == st and st > 0 and 0 < bp < bt and set(solutions) == set(broken)
        ok = ok and good
        print(
            "%-4s %-32s solution %d/%d   broken %d/%d"
            % ("OK" if good else "BAD", name, sp, st, bp, bt)
        )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
