#!/usr/bin/env python3
"""THE HOLLOW LINE. Run:  python play.py   (python3 on macOS/Linux)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hollowline.main import main  # noqa: E402

if __name__ == "__main__":
    main()
