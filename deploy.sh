#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

./venv/bin/python -m ensurepip --upgrade || true
./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r requirements.txt

echo "Done. Now copy .env.example to .env and add BOT_TOKEN."
