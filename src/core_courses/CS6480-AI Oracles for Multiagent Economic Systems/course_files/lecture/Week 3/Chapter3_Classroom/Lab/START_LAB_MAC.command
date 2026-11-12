#!/bin/sh
# Copyright © 2026 Xiaotie Deng. City University of Hong Kong.
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$LAB_DIR"
if ! command -v python3 >/dev/null 2>&1; then
  printf 'Python 3.8 or later is required. Please ask the instructor or TA.\n'
  printf 'Press Return to close.\n'
  read -r answer
  exit 1
fi
python3 chapter3_lab.py "$@"
if [ -t 0 ]; then printf '\nPress Return to close.\n'; read -r answer || true; fi
