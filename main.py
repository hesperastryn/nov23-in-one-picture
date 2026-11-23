#!/usr/bin/env python3
"""Entrypoint for the grading sandbox.

The grader runs this file with a bare standard-library interpreter:
no PIL, no network, the repository mounted read-only. So the entry
point does exactly one thing — copy the committed entry.png (which
generate.py produced ahead of time) into MAKEFUN_OUTPUT_DIR.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR unset; entry.png already in place")
        return 0
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    if os.path.abspath(dest) != os.path.abspath(src):
        shutil.copyfile(src, dest)
    print("entry.png ->", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
