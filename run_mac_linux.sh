#!/usr/bin/env sh
# THE HOLLOW LINE launcher for macOS / Linux
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
    exec python3 play.py "$@"
else
    exec python play.py "$@"
fi
