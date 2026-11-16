#!/usr/bin/env python3
"""Derive the broken implementation of a test from its reference solution.

Reads   .reference/<name>/solution_<module>.py
        .reference/<name>/bugs.py      (defines BUGS, see below)
Writes  .reference/<name>/broken/<module>.py
        .reference/<name>/BUGS.md
        tests/<name>/<module>.py       (only if missing, or with --force)

bugs.py defines a list of dicts, one per planted bug:

    BUGS = [
        dict(where="tokenize, digits", bug="sums the digits",
             fix="num * 10 + int(ch)",
             find="num = num * 10 + int(ch)", replace="num = num + int(ch)"),
    ]

Each `find` must occur exactly once in the solution, so every bug is a
small, local, reviewable change.

    python3 scripts/plant.py 03 [--force]
"""
import os
import runpy
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if len(args) != 1:
        sys.exit(__doc__)
    ref_root = os.path.join(ROOT, ".reference")
    matches = sorted(
        d for d in os.listdir(ref_root)
        if d.startswith(args[0]) and os.path.isdir(os.path.join(ref_root, d))
    )
    if len(matches) != 1:
        sys.exit("expected exactly one .reference/%s* folder, found: %s" % (args[0], matches))
    name = matches[0]
    ref = os.path.join(ref_root, name)
    solutions = [f for f in os.listdir(ref) if f.startswith("solution_") and f.endswith(".py")]
    if len(solutions) != 1:
        sys.exit("expected exactly one solution_*.py in %s" % ref)
    module = solutions[0][len("solution_"):]
    with open(os.path.join(ref, solutions[0])) as f:
        source = f.read()
    bugs = runpy.run_path(os.path.join(ref, "bugs.py"))["BUGS"]

    for n, bug in enumerate(bugs, 1):
        if source.count(bug["find"]) != 1:
            sys.exit("bug %d: `find` occurs %d times, need exactly 1:\n%s"
                     % (n, source.count(bug["find"]), bug["find"]))
    broken = source
    for n, bug in enumerate(bugs, 1):
        if broken.count(bug["find"]) != 1:
            sys.exit("bug %d overlaps an earlier bug" % n)
        broken = broken.replace(bug["find"], bug["replace"])

    os.makedirs(os.path.join(ref, "broken"), exist_ok=True)
    with open(os.path.join(ref, "broken", module), "w") as f:
        f.write(broken)

    lines = ["# %s — planted bugs (%d)" % (name, len(bugs)), "",
             "| # | Where | Bug | Fix |", "|---|-------|-----|-----|"]
    for n, bug in enumerate(bugs, 1):
        cells = [str(bug[k]).replace("|", "\\|") for k in ("where", "bug", "fix")]
        lines.append("| %d | %s | %s | %s |" % (n, cells[0], cells[1], cells[2]))
    with open(os.path.join(ref, "BUGS.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    test_dir = os.path.join(ROOT, "tests", name)
    os.makedirs(test_dir, exist_ok=True)
    target = os.path.join(test_dir, module)
    if "--force" in sys.argv or not os.path.exists(target):
        with open(target, "w") as f:
            f.write(broken)
        print("wrote tests/%s/%s" % (name, module))
    else:
        print("kept existing tests/%s/%s (use --force to overwrite)" % (name, module))
    print("planted %d bugs in %s" % (len(bugs), name))


if __name__ == "__main__":
    main()
