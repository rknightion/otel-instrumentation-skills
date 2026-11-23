#!/bin/sh
# Start upstream.py on Python 3.15: python3.15 on PATH, then the Homebrew
# locations, then uv. With none of them, exit 1 and say how to get 3.15.
case "$0" in
  */*) here=${0%/*} ;;
  *) here=. ;;
esac
script=$here/upstream.py

if command -v python3.15 >/dev/null 2>&1; then
  exec python3.15 "$script" "$@"
fi
for py in /opt/homebrew/bin/python3.15 /home/linuxbrew/.linuxbrew/bin/python3.15; do
  if [ -x "$py" ]; then
    exec "$py" "$script" "$@"
  fi
done
if command -v uv >/dev/null 2>&1; then
  exec uv run --no-project --python 3.15 "$script" "$@"
fi
echo "upstream.sh: Python 3.15 or newer is required and was not found. Install it with 'brew install python@3.15', or install uv and run 'uv python install 3.15', then rerun." >&2
exit 1
