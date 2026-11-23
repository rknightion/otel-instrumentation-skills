#!/bin/sh
# Start upstream.py on Python 3.15: python3.15 on PATH, then the Homebrew
# locations, then an interpreter resolved by uv. With none of them, exit 1 and
# say how to get 3.15.
#
# uv only resolves a path, from / with its project, config and environment
# hints cleared, so a .venv, uv.toml or VIRTUAL_ENV in the caller's directory
# can never choose what runs. The tool itself is exec'd from the caller's
# directory, never through uv run.
case "$0" in
  */*) here=${0%/*} ;;
  *) here=. ;;
esac
script=$here/upstream.py

# Accept only an absolute path to an executable that is not a virtualenv interpreter.
usable() {
  case "$1" in
    /*) ;;
    *) return 1 ;;
  esac
  case "$1" in
    */.venv/*) return 1 ;;
  esac
  [ -x "$1" ] || return 1
  [ ! -f "${1%/*}/../pyvenv.cfg" ] || return 1
}

uv_resolve() {
  (
    cd / || exit 1
    unset VIRTUAL_ENV CONDA_PREFIX UV_PYTHON UV_PROJECT_ENVIRONMENT
    uv "$@" </dev/null 2>/dev/null
  )
}

py=$(command -v python3.15 2>/dev/null)
if usable "$py"; then
  exec "$py" "$script" "$@"
fi
for py in /opt/homebrew/bin/python3.15 /home/linuxbrew/.linuxbrew/bin/python3.15; do
  if usable "$py"; then
    exec "$py" "$script" "$@"
  fi
done
if command -v uv >/dev/null 2>&1; then
  py=$(uv_resolve python find --no-project --no-config --no-python-downloads 3.15)
  if ! usable "$py"; then
    uv_resolve python install --no-config 3.15 >/dev/null
    py=$(uv_resolve python find --no-project --no-config --no-python-downloads 3.15)
  fi
  if usable "$py"; then
    exec "$py" "$script" "$@"
  fi
fi
echo "upstream.sh: Python 3.15 or newer is required and was not found. Install it with 'brew install python@3.15', or install uv and run 'uv python install 3.15', then rerun." >&2
exit 1
