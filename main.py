#!/usr/bin/env python3
# Entry program for the make.fun competition news-image-20261123,
# "Sum up 23 November's world news in one image".
#
# The picture is drawn ahead of time by generate.py (PIL) and committed
# next to this file as entry.png. This program is standard-library only:
# it copies that committed PNG into the output directory (the one named
# by MAKEFUN_OUTPUT_DIR, default /output), so every grading run yields
# exactly the same bytes.
"""Copy the committed entry.png to the grading output directory."""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
