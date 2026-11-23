#!/bin/sh
# Start upstream.py on Python 3.15: python3.15 on PATH, then the Homebrew
# locations, then an interpreter resolved by uv. With none of them, exit 1 and
# say how to get 3.15.
#
# PATH is walked here and only absolute directories count, so "." or an empty
# PATH element can never run a file from the caller's directory. uv only
# resolves a path, from / with its project, config and environment hints
# cleared, so a .venv, uv.toml, VIRTUAL_ENV or UV_WORKING_DIR in the caller's
# directory can never choose what runs. The tool itself is exec'd from the
# caller's directory, never through uv run.
case "$0" in
  */*) here=${0%/*} ;;
  *) here=. ;;
esac
script=$here/upstream.py

# Print the first usable $1 found in an absolute PATH directory; a rejected
# candidate (a virtualenv interpreter) moves on to the next entry.
find_in_path() {
  rest=$PATH:
  while [ -n "$rest" ]; do
    dir=${rest%%:*}
    rest=${rest#*:}
    case "$dir" in
      /*)
        if [ -f "$dir/$1" ] && usable "$dir/$1"; then
          printf '%s\n' "$dir/$1"
          return 0
        fi
        ;;
    esac
  done
  return 1
}

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
    unset VIRTUAL_ENV CONDA_PREFIX UV_PYTHON UV_PROJECT_ENVIRONMENT UV_WORKING_DIR
    "$uv" --directory / "$@" </dev/null 2>/dev/null
  )
}

py=$(find_in_path python3.15)
if usable "$py"; then
  exec "$py" "$script" "$@"
fi
for py in /opt/homebrew/bin/python3.15 /home/linuxbrew/.linuxbrew/bin/python3.15; do
  if usable "$py"; then
    exec "$py" "$script" "$@"
  fi
done
uv=$(find_in_path uv)
case "$uv" in
  /*)
    py=$(uv_resolve python find --no-project --no-config --no-python-downloads 3.15)
    if ! usable "$py"; then
      uv_resolve python install --no-config 3.15 >/dev/null
      py=$(uv_resolve python find --no-project --no-config --no-python-downloads 3.15)
    fi
    if usable "$py"; then
      exec "$py" "$script" "$@"
    fi
    ;;
esac
echo "upstream.sh: Python 3.15 or newer is required and was not found. Install it with 'brew install python@3.15', or install uv and run 'uv python install 3.15', then rerun." >&2
exit 1
