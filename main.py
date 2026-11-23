#!/usr/bin/env python3
"""Entrypoint: regenerate the front page into MAKEFUN_OUTPUT_DIR.

Runs generate.py's main() with the output directory taken from the
environment, so the platform can rebuild entry.png on demand.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate import main

if __name__ == "__main__":
    main()
